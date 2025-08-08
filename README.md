# Kafka Docker Setup

[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![Kafka](https://img.shields.io/badge/Apache%20Kafka-3.5+-orange.svg)](https://kafka.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

I've created a complete Apache Kafka development environment using Docker Compose with all essential components for data streaming and processing. This setup includes everything you need to get started with Kafka development.

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Services Overview](#-services-overview)
- [Management Commands](#️-management-commands)
- [Monitoring & Management](#-monitoring--management)
- [Example Usage](#-example-usage)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Additional Resources](#-additional-resources)
- [Contributing](#-contributing)

## ✨ Features

- 🐳 **Complete Docker Setup** - All services containerized and ready to run
- 📊 **Kafka UI Dashboard** - Web-based management interface
- 🔌 **Kafka Connect** - Data streaming and ETL capabilities
- 📋 **Schema Registry** - Avro schema management
- 📈 **JMX Monitoring** - Built-in monitoring and metrics
- 🔄 **Auto Topic Creation** - Development-friendly configuration
- 💾 **Persistent Storage** - Data persistence across restarts

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Hub account (for pulling images)

### Setup Instructions

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd Kafka
   ```

2. **Start Docker Desktop**
   ```bash
   open -a Docker
   ```

3. **Login to Docker Hub** (if not already logged in)
   ```bash
   docker login
   ```

4. **Start all services**
   ```bash
   docker-compose up -d
   ```

5. **Verify services are running**
   ```bash
   docker-compose ps
   ```

6. **Access Kafka UI Dashboard**
   - Open your browser and go to: **http://localhost:8080**

## 📋 Services Overview

I've configured the following core services for your Kafka environment:

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| **Zookeeper** | 2181 | Cluster coordination and metadata management |
| **Kafka Broker** | 9092, 9101 | Message broker with JMX monitoring |
| **Schema Registry** | 8081 | Avro schema management and validation |
| **Kafka Connect** | 8083 | Data streaming and ETL operations |
| **Kafka UI** | 8080 | Web-based Kafka management interface |

### Service Details

#### 🐘 Zookeeper
- **Image**: `confluentinc/cp-zookeeper:7.4.0`
- **Purpose**: Manages Kafka cluster coordination and metadata
- **Access**: `localhost:2181`

#### 📨 Kafka Broker
- **Image**: `confluentinc/cp-kafka:7.4.0`
- **Purpose**: Message broker for publishing and subscribing to data streams
- **Access**: 
  - External: `localhost:9092`
  - Internal: `kafka:29092`
  - JMX: `localhost:9101`

#### 📊 Schema Registry
- **Image**: `confluentinc/cp-schema-registry:7.4.0`
- **Purpose**: Manages Avro schemas for data serialization
- **Access**: `localhost:8081`

#### 🔌 Kafka Connect
- **Image**: `confluentinc/cp-kafka-connect:7.4.0`
- **Purpose**: Data streaming platform for ETL operations
- **Access**: `localhost:8083`

#### 🖥️ Kafka UI
- **Image**: `provectuslabs/kafka-ui:latest`
- **Purpose**: Web interface for managing topics, consumers, and monitoring
- **Access**: `http://localhost:8080`

## 🛠️ Management Commands

Here are the essential commands I use to manage your Kafka services:

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs kafka
docker-compose logs zookeeper
```

### Restart Services
```bash
docker-compose restart
```

### Remove Everything (including volumes)
```bash
docker-compose down -v
```

## 🔍 Monitoring & Management

I've set up comprehensive monitoring for your Kafka cluster:

### Kafka UI Dashboard
- **URL**: http://localhost:8080
- **Features**:
  - Topic management
  - Consumer group monitoring
  - Message browsing
  - Schema registry integration

### JMX Monitoring
- **Port**: 9101
- **Use with**: JConsole, VisualVM, or other JMX tools

## 📝 Example Usage

I've prepared these practical examples to help you get started with Kafka operations:

### 1. Creating Topics
```bash
# Create a new topic
docker exec kafka kafka-topics --create \
  --topic "my-first-topic" \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

### 2. Listing Topics
```bash
# List all topics
docker exec kafka kafka-topics --list \
  --bootstrap-server localhost:9092
```

### 3. Producing Messages
```bash
# Start an interactive producer
docker exec -it kafka kafka-console-producer \
  --topic "my-first-topic" \
  --bootstrap-server localhost:9092
```
**Note**: This opens an interactive console where you can type messages and press Enter to send them.

### 4. Consuming Messages
```bash
# Start a consumer to read messages
docker exec -it kafka kafka-console-consumer \
  --topic "my-first-topic" \
  --bootstrap-server localhost:9092 \
  --from-beginning
```
**Note**: The `--from-beginning` flag reads all messages from the start of the topic.

### 5. Deleting Topics
```bash
# Delete a topic
docker exec kafka kafka-topics --delete \
  --topic "my-first-topic" \
  --bootstrap-server localhost:9092
```

## 🎯 Kafka CLI Basics Tutorial

### Step-by-Step Example

1. **Create a topic:**
   ```bash
   docker exec kafka kafka-topics --create --topic "my-first-topic" --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

2. **Verify topic creation:**
   ```bash
   docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
   ```

3. **Start a producer (in one terminal):**
   ```bash
   docker exec -it kafka kafka-console-producer --topic "my-first-topic" --bootstrap-server localhost:9092
   ```
   Then type messages and press Enter:
   ```
   > Hello Kafka!
   > This is my first message
   > Learning Kafka is fun!
   ```

4. **Start a consumer (in another terminal):**
   ```bash
   docker exec -it kafka kafka-console-consumer --topic "my-first-topic" --bootstrap-server localhost:9092 --from-beginning
   ```

5. **Clean up when done:**
   ```bash
   docker exec kafka kafka-topics --delete --topic "my-first-topic" --bootstrap-server localhost:9092
   ```

6. **Verify topic deletion:**
   ```bash
   docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
   ```
   The topic should no longer appear in the list.

### Expected Output Examples

**Topic Creation:**
```bash
$ docker exec kafka kafka-topics --create --topic "my-first-topic" --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
Created topic my-first-topic.
```

**Producer Session:**
```bash
$ docker exec -it kafka kafka-console-producer --topic "my-first-topic" --bootstrap-server localhost:9092
>hello from producer
>hi my name is basanth
>learning kafka is awesome!
>^C  # Press Ctrl+C to exit
```

**Consumer Output:**
```bash
$ docker exec -it kafka kafka-console-consumer --topic "my-first-topic" --bootstrap-server localhost:9092 --from-beginning
hello from producer
hi my name is basanth
learning kafka is awesome!
^C  # Press Ctrl+C to exit
```

**Topic Deletion:**
```bash
$ docker exec kafka kafka-topics --delete --topic "my-first-topic" --bootstrap-server localhost:9092
# Command completes silently if successful
```

**Verification After Deletion:**
```bash
$ docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
__consumer_offsets
_schemas
docker-connect-configs
docker-connect-offsets
docker-connect-status
# Note: "my-first-topic" is no longer listed
```

### Important Notes for Docker Users

- **Always prefix commands** with `docker exec kafka`
- **Use `docker exec -it`** for interactive commands (producer/consumer)
- **No `.sh` extension** needed in Docker containers
- **Use `localhost:9092`** as the bootstrap server
- **Silent success**: Topic deletion commands don't show output on success
- **Verify operations**: Always list topics to confirm creation/deletion

## 🔍 Explore How Kafka Works

### Understanding Kafka Architecture

Let's dive deeper into how Kafka stores and manages data by exploring the internal structure.

#### 1. Topic Storage Exploration

Create a topic to examine its internal structure:
```bash
docker exec kafka kafka-topics --create --topic kafka-arch --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
```

#### 2. Inspecting the Directory Structure

Explore how Kafka stores data on disk:
```bash
# Look at the Kafka data directory
docker exec kafka ls /var/lib/kafka/data/

# Examine the topic-specific directory
docker exec kafka ls -alh /var/lib/kafka/data/kafka-arch*
```

**What you'll see:**
- Kafka creates a directory for each topic-partition combination
- Files include `.log` (actual data), `.index` (message index), and `.timeindex` (time-based index)
- Initially, the `.log` file will be empty since no messages have been produced

#### 3. Produce Data and Observe Changes

Add some data to see how Kafka stores it:
```bash
# Start producer
docker exec -it kafka kafka-console-producer --topic "kafka-arch" --bootstrap-server localhost:9092
```

Produce 5-10 messages:
```
> Message 1: Learning Kafka architecture
> Message 2: Understanding partitions
> Message 3: Exploring data storage
> Message 4: Kafka is powerful
> Message 5: Data persistence in action
> ^C  # Exit with Ctrl+C
```

Now check the log file:
```bash
# View the log file content (binary format)
docker exec kafka ls -alh /var/lib/kafka/data/kafka-arch*

# Check file sizes - you should see the .log file has grown
docker exec kafka du -h /var/lib/kafka/data/kafka-arch*
```

#### 4. Topics and Partitions

Explore partition scaling:
```bash
# Increase partitions from 1 to 3
docker exec kafka kafka-topics --alter --topic kafka-arch --partitions 3 --bootstrap-server localhost:9092

# Verify the change
docker exec kafka kafka-topics --describe --topic kafka-arch --bootstrap-server localhost:9092

# See new directories created
docker exec kafka ls -alh /var/lib/kafka/data/kafka-arch*
```

**What happens:**
- Kafka creates additional partition directories (`kafka-arch-1`, `kafka-arch-2`)
- New messages will be distributed across all partitions
- Existing messages remain in their original partition

#### 5. Understanding the Architecture

**Key Concepts Demonstrated:**

- **Kafka Broker**: An individual Kafka server (you have 1 in your Docker setup)
- **Kafka Cluster**: A group of Kafka Brokers working together
- **Zookeeper Role**: Coordinates brokers and manages cluster metadata
- **Persistent Storage**: Kafka writes log files directly to disk on brokers
- **Partitioning**: Enables scale and parallelism by distributing data
- **Replication**: Provides fault tolerance (set to 1 in development)

#### 6. Clean Up

Remove the exploration topic when done:
```bash
docker exec kafka kafka-topics --delete --topic kafka-arch --bootstrap-server localhost:9092
```

### Architecture Insights

This exploration reveals how Kafka achieves:

- **📈 Scale & Parallelism**: Through topic partitions that can be distributed across brokers
- **🛡️ Resiliency**: Via data replication across multiple brokers (production setup)
- **💾 Persistence**: By writing all data to disk in structured log files
- **⚡ Performance**: Using efficient file system operations and zero-copy reads

## 🔧 Configuration

I've configured the following settings for optimal development experience:

### Environment Variables
Key configuration options in `docker-compose.yaml`:

- `KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'` - Auto-create topics
- `KAFKA_DELETE_TOPIC_ENABLE: 'true'` - Allow topic deletion
- `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1` - Single broker setup

### Volumes
I've set up persistent data storage in Docker volumes:
- `zookeeper-data` - Zookeeper data
- `zookeeper-logs` - Zookeeper logs
- `kafka-data` - Kafka data
- `kafka-connect-data` - Kafka Connect data

## 🚨 Troubleshooting

I've encountered and solved these common issues during setup:

### Common Issues

1. **Docker Hub Authentication**
   ```bash
   docker login
   ```

2. **Port Already in Use**
   - Check if ports 2181, 9092, 8080, 8081, 8083 are available
   - Stop conflicting services

3. **Services Not Starting**
   ```bash
   docker-compose logs
   ```

4. **Permission Issues**
   ```bash
   sudo chown -R $USER:$USER .
   ```

### Health Checks
I use these commands to verify everything is working properly:
```bash
# Check service status
docker-compose ps

# Check individual service health
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

## 🖼️ Screenshots

### Kafka UI Dashboard
![Kafka UI Dashboard](images/kafka_UI.png)

The Kafka UI provides a comprehensive web interface for managing your Kafka cluster, showing:
- **Broker Information**: Active brokers, uptime, and partition details
- **Cluster Health**: Real-time monitoring of your Kafka cluster
- **Navigation Menu**: Easy access to Topics, Consumers, and other management features

## 📊 Project Structure

```
Kafka/
├── docker-compose.yaml    # Main Docker Compose configuration
├── README.md             # This documentation
└── images/               # Screenshots and diagrams (add your images here)
    ├── kafka-ui-dashboard.png
    ├── topic-management.png
    └── schema-registry.png
```

## 🧪 Testing

I've included some basic tests to verify your setup:

```bash
# Test Kafka connectivity
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# Test topic creation
docker exec kafka kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Test message production
echo "Hello Kafka!" | docker exec -i kafka kafka-console-producer --topic test-topic --bootstrap-server localhost:9092

# Test message consumption
docker exec kafka kafka-console-consumer --topic test-topic --from-beginning --bootstrap-server localhost:9092 --max-messages 1
```

## 🔧 Advanced Configuration

### Custom Environment Variables

You can customize the setup by modifying the environment variables in `docker-compose.yaml`:

```yaml
environment:
  KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
  KAFKA_DELETE_TOPIC_ENABLE: 'true'
  KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

### Adding Custom Connectors

To add custom Kafka Connect connectors:

1. Create a `connectors/` directory
2. Add your connector JAR files
3. Mount the directory in the kafka-connect service

## 🚀 Deployment

### Local Development
```bash
docker-compose up -d
```

### Production Considerations
- Use external storage volumes
- Implement security (SASL/SSL)
- Set up monitoring and alerting
- Configure proper replication factors
- Use managed Kafka services (AWS MSK, Confluent Cloud, etc.)


## 🙏 Acknowledgments

- [Apache Kafka](https://kafka.apache.org/) - The distributed streaming platform
- [Confluent](https://www.confluent.io/) - Kafka platform and tools
- [Kafka UI](https://github.com/provectus/kafka-ui) - Web interface for Kafka management

---

**Note**: I've configured this setup for development purposes. For production use, consider:
- Increasing replication factors
- Adding security configurations
- Using external storage
- Implementing proper monitoring and alerting 