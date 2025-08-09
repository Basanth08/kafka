#!/usr/bin/env python3
"""
Advanced Kafka Consumer with Error Handling, Metrics, Storage, and Alerts
Author: Basanth Varaganti
"""

from kafka import KafkaConsumer
from kafka.errors import KafkaError, CommitFailedError
import json
import logging
import time
import sqlite3
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass
import os

# Configuration
@dataclass
class ConsumerConfig:
    bootstrap_servers: str = 'localhost:9092'
    group_id: str = 'AdvancedCountryCounter'
    topic: str = 'customerCountries'
    auto_offset_reset: str = 'earliest'
    enable_auto_commit: bool = False
    max_poll_records: int = 10
    poll_timeout_ms: int = 1000

# Metrics Class
class ConsumerMetrics:
    def __init__(self):
        self.message_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.last_message_time = time.time()
        self.processing_times = []
    
    def record_message(self, processing_time):
        self.message_count += 1
        self.last_message_time = time.time()
        self.processing_times.append(processing_time)
    
    def record_error(self):
        self.error_count += 1
    
    def get_stats(self):
        runtime = time.time() - self.start_time
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
        
        return {
            'total_messages': self.message_count,
            'total_errors': self.error_count,
            'runtime_seconds': runtime,
            'messages_per_second': self.message_count / runtime if runtime > 0 else 0,
            'avg_processing_time_ms': avg_processing_time * 1000,
            'last_message_ago': time.time() - self.last_message_time
        }

# Data Storage Class
class DataStore:
    def __init__(self):
        self.conn = sqlite3.connect('kafka_data.db')
        self.create_tables()
        
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS country_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT,
                timestamp TEXT,
                partition INTEGER,
                offset INTEGER
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS country_counts (
                country TEXT PRIMARY KEY,
                count INTEGER,
                last_updated TEXT
            )
        ''')
        self.conn.commit()
    
    def store_message(self, country, partition, offset):
        timestamp = datetime.now().isoformat()
        self.conn.execute('''
            INSERT INTO country_messages (country, timestamp, partition, offset)
            VALUES (?, ?, ?, ?)
        ''', (country, timestamp, partition, offset))
        
        self.conn.execute('''
            INSERT OR REPLACE INTO country_counts (country, count, last_updated)
            VALUES (?, 
                COALESCE((SELECT count FROM country_counts WHERE country = ?), 0) + 1,
                ?)
        ''', (country, country, timestamp))
        
        self.conn.commit()
    
    def get_top_countries(self, limit=5):
        cursor = self.conn.execute('''
            SELECT country, count FROM country_counts 
            ORDER BY count DESC LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

# Alert System Class
class AlertSystem:
    def __init__(self):
        self.thresholds = {
            'max_messages_per_country': 50,
            'max_error_rate': 0.1,
            'max_processing_time': 1.0
        }
    
    def check_alerts(self, country_counts, metrics):
        alerts = []
        
        for country, count in country_counts.items():
            if count > self.thresholds['max_messages_per_country']:
                alerts.append(f"⚠️  High volume for {country}: {count} messages")
        
        total_messages = metrics.message_count
        if total_messages > 0:
            error_rate = metrics.error_count / total_messages
            if error_rate > self.thresholds['max_error_rate']:
                alerts.append(f"🚨 High error rate: {error_rate:.2%}")
        
        return alerts

# Main Consumer Class
class AdvancedKafkaConsumer:
    def __init__(self, config: ConsumerConfig):
        self.config = config
        self.setup_logging()
        self.metrics = ConsumerMetrics()
        self.data_store = DataStore()
        self.alert_system = AlertSystem()
        self.country_counts = defaultdict(int)
        
        # Valid countries list
        self.valid_countries = [
            'USA', 'Canada', 'UK', 'Germany', 'India', 'France', 
            'Japan', 'Australia', 'Brazil', 'Mexico', 'China', 'Russia'
        ]
        
        self.consumer = KafkaConsumer(
            bootstrap_servers=[config.bootstrap_servers],
            group_id=config.group_id,
            key_deserializer=lambda m: m.decode('utf-8') if m else None,
            value_deserializer=lambda m: m.decode('utf-8'),
            auto_offset_reset=config.auto_offset_reset,
            enable_auto_commit=config.enable_auto_commit,
            max_poll_records=config.max_poll_records
        )
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_message(self, message):
        """Validate message format and content"""
        try:
            if message.value not in self.valid_countries:
                self.logger.warning(f"Unknown country: {message.value}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False
    
    def process_message(self, message):
        """Process individual message with full pipeline"""
        start_time = time.time()
        
        try:
            # Validate message
            if not self.validate_message(message):
                return
            
            country = message.value
            
            # Update in-memory counters
            self.country_counts[country] += 1
            
            # Store in database
            self.data_store.store_message(
                country, message.partition, message.offset
            )
            
            # Record metrics
            processing_time = time.time() - start_time
            self.metrics.record_message(processing_time)
            
            # Log processed message
            self.logger.info(f"Processed: {country} (Total: {self.country_counts[country]})")
            
        except Exception as e:
            self.metrics.record_error()
            self.logger.error(f"Error processing message: {e}")
            raise e
    
    def print_status(self):
        """Print current status and metrics"""
        print("\n" + "="*60)
        print(f"🌍 Current Country Counts:")
        print(json.dumps(dict(self.country_counts), indent=2))
        
        print(f"\n📊 Consumer Metrics:")
        print(json.dumps(self.metrics.get_stats(), indent=2))
        
        # Top countries from database
        top_countries = self.data_store.get_top_countries()
        print(f"\n🏆 Top Countries (Database):")
        for country, count in top_countries:
            print(f"  {country}: {count}")
        
        # Check alerts
        alerts = self.alert_system.check_alerts(self.country_counts, self.metrics)
        if alerts:
            print(f"\n🚨 ALERTS:")
            for alert in alerts:
                print(f"  {alert}")
        
        print("="*60)
    
    def run(self):
        """Main consumer loop"""
        self.logger.info("Starting Advanced Kafka Consumer...")
        self.consumer.subscribe([self.config.topic])
        
        try:
            while True:
                try:
                    records = self.consumer.poll(timeout_ms=self.config.poll_timeout_ms)
                    
                    if not records:
                        print("⏳ Waiting for messages...")
                        continue
                    
                    # Process all messages
                    for topic_partition, messages in records.items():
                        for message in messages:
                            self.process_message(message)
                    
                    # Commit after successful processing
                    self.consumer.commit()
                    
                    # Print status every 5 messages
                    if self.metrics.message_count % 5 == 0:
                        self.print_status()
                    
                except CommitFailedError as e:
                    self.logger.error(f"Commit failed: {e}")
                except KafkaError as e:
                    self.logger.error(f"Kafka error: {e}")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            self.logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()
            self.logger.info("Consumer closed successfully!")

# Main execution
if __name__ == "__main__":
    config = ConsumerConfig()
    consumer = AdvancedKafkaConsumer(config)
    consumer.run() 