# Part 2 - Cloud, Security and IoT Deployment Blueprint

## Task 9 - Distributed Architecture and Communication Plan

### Chosen Architecture: Client-Server

I choose a Client-Server architecture for the Smart City platform. The three
zone controllers act as clients and communicate with a central Smart City
Operations Dashboard/server.
The scheduler and safety engine from Part 1 will run as the compute engine
inside the central cloud platform.
The main reasons for choosing Client-Server are:
1. **Transparency:** The zone controllers do not need to know how the central
   scheduling and safety engine works. They only send data and receive results.
2. **Fault tolerance:** If one zone controller fails, the other zone
   controllers can continue sending data to the central system.
3. **Scalability:** More zone controllers can be added later without changing
   the complete architecture. The central server can also be scaled when the
   number of sensors increases.
4. **Single point of control:** The Smart City Operations Dashboard provides
   one place for operators to monitor the three zones and the results produced
   by the Part 1 scheduler and safety engine.

### Data Flow 1 - Real-Time Public-Safety Alert
When a zone controller detects a serious public-safety event, it sends an alert
to the Smart City Operations Dashboard.
I would use **asynchronous communication** because the controller should not
have to wait while the dashboard processes the alert.
The protocol would be **MQTT over TLS**. MQTT is suitable for IoT devices
because it has low communication overhead and supports publish/subscribe
messaging. TLS protects the alert while it is being transmitted.
The flow is:
Zone Controller -> MQTT/TLS -> Cloud Platform -> Operations Dashboard
The Part 1 scheduler can process sensor-processing jobs in the cloud platform,
while the safety engine can check resource safety when required.
### Data Flow 2 - Full-Day Sensor Log
For uploading a complete day's sensor log, I would also use
**asynchronous communication**. A large file does not need an immediate
response from the dashboard.
The zone controller can upload the file using **HTTPS** to cloud storage.
The transfer is protected using TLS.
The flow is:
Zone Controller -> HTTPS/TLS -> Cloud Storage -> Cloud Processing -> Dashboard
This approach keeps large sensor files separate from the real-time alert
channel.

## Task 10 - VPC-Based Network Boundary
I would use **one VPC containing three separate subnets**, one for each smart
city zone:
- Zone-A subnet
- Zone-B subnet
- Zone-C subnet
The three zones are logically isolated even though they are inside the same
VPC.
The reason for using one VPC is that the zones are part of the same city
platform and need controlled communication with common cloud services.
Separate subnets make the network easier to manage while still providing
logical isolation.
The VPC also provides custom routing and security controls. Each zone subnet
can have its own firewall/security-group rules.
The specific network-level control I would use is a **firewall/security-group
rule** that denies direct traffic from the Zone-B subnet to Zone-A resources.
For example:
`Zone-B subnet -> DENY -> Zone-A resources`
Only approved traffic through the required cloud services is allowed.
The Smart City Operations Dashboard is not itself the control that creates
this boundary. The network firewall/security-group rule is the actual
network-level control.

## Task 11 - Network Security Objectives and Controls
### 1. Protect Sensitive Data
I would use **encryption at rest** for sensor logs, job information and
other stored city data.
This prevents someone who gets access to the storage system from reading the
stored information directly.
### 2. Authentication
I would use **TLS certificates and authenticated identities** for zone
controllers.
Only registered zone controllers should be allowed to send data to the
cloud platform.
### 3. Authorization
I would use **IAM roles with least-privilege permissions**.
For example, a zone controller should only have permission to upload its own
sensor data and should not have permission to modify another zone's data.
### 4. Prevent Cyber Attacks
I would use a **network firewall/security group together with an intrusion
detection system**.
The firewall can block unwanted network traffic while intrusion detection
can identify suspicious activity.
### 5. Secure Communication
I would use **TLS encryption** for communication between zone controllers and
the cloud platform.
This protects sensor information and public-safety alerts while they travel
over the network.
### 6. Ensure Availability
I would use **redundant cloud instances and automatic recovery** for important
services.
If one application instance fails, another instance can continue processing
the requests.

## Task 12 - IAM Table and Data Protection Map
### I AM Roles
| Role | Permissions |
|---|---|
| Zone Operator | View and manage jobs and sensor information for the assigned zone |
| City Dashboard Admin | View all zones, manage dashboard settings and monitor alerts |
| Auditor | Read logs and security records but cannot modify operational data |
The permissions are intentionally different so that every user receives only
the access needed for their job.
### Data Protection Map
| Data State | Example from Platform | Protection |
|---|---|---|
| At Rest | `JOBS` list or stored sensor log on a zone controller/cloud storage | Encryption at rest |
| In Transit | Public-safety alert sent to the dashboard | TLS encryption |
| In Use | Banker's Algorithm safety check running in memory | Access-controlled application memory |
The fixed `JOBS` data from Part 1 can be stored using encryption at rest.
A public-safety alert generated by a zone controller is protected with TLS
while travelling to the dashboard.
The Banker's-Algorithm safety check from Part 1 operates in application
memory, so access to the process and its memory should be restricted to the
authorized scheduling service.

## Task 13 - IoT Connectivity and Architecture Layers
The platform can use different communication technologies depending on the
type of sensor.
### Sensor and Communication Mapping
| Device Type | Communication Technology | Reason |
|---|---|---|
| Traffic camera trigger | 5G | High bandwidth and suitable for moving or frequently connected devices |
| Environmental sensor | LoRaWAN | Long range and low power consumption |
| Wearable public-safety device | Bluetooth | Short-range and low-power connection to a nearby gateway |
### IoT Architecture Layers
#### 1. Physical Environment
This layer represents the real-world smart-city environment, such as roads,
traffic areas, public spaces and environmental conditions.
#### 2. Perception / Device Layer
This layer contains the actual sensors and devices, such as traffic-camera
triggers, environmental sensors and wearable safety devices.
#### 3. Gateway Layer
Gateways collect information from local devices and forward it toward the
cloud platform.
For example, a gateway can collect Bluetooth wearable data before sending it
to the cloud.
#### 4. Network Communication Layer
This layer provides communication between gateways, zone controllers and
cloud services using technologies such as 5G, LoRaWAN, Wi-Fi and secure
Internet connections.
#### 5. Cloud Platform Layer
The **scheduler and safety engine from Part 1** are used as the Cloud
Platform Layer.
This includes the fixed `JOBS` list, FCFS/SJF/SRTF scheduling, Round Robin,
Priority Scheduling, Peterson's Algorithm, Banker's Algorithm and the paging
and segmentation address translator.
#### 6. Application Layer
The Smart City Operations Dashboard belongs to the application layer.
It displays information from the three zones and allows authorized city
operators to monitor alerts, jobs and system status.

## Task 14 - Threats and Mitigations
### Threat 1 - Unauthorized Access to Zone Data
An attacker could obtain access to one zone's sensor information and try to
access another zone.
**Mitigation:** Use IAM least-privilege permissions and firewall/security-group
rules to restrict cross-zone access.
### Threat 2 - Man-in-the-Middle Attack
An attacker could attempt to intercept sensor data or public-safety alerts
while they are travelling from a zone controller to the cloud.
**Mitigation:** Use TLS for communication between zone controllers, gateways
and cloud services.
### Threat 3 - Denial-of-Service Attack
An attacker could send a large number of requests to the cloud service and
make the dashboard or scheduler unavailable.
**Mitigation:** Use firewall rules, rate limiting and redundant cloud
instances so that abnormal traffic can be filtered and the service can
continue operating.
### Threat 4 - Compromised IoT Device
A compromised sensor or zone controller could send false or malicious data
to the platform.
**Mitigation:** Use device authentication, certificate-based identity and
only allow registered devices to communicate with the platform.

# Conclusion

The proposed Client-Server architecture provides a central and manageable
platform for the three smart-city zones. The three zone subnets provide
logical network isolation, while IAM, encryption, TLS and firewall controls
protect the platform.

The scheduler and safety engine developed in Part 1 remain the fixed compute
core of the design. The cloud platform can therefore process the same
sensor-processing jobs and use the same scheduling, synchronization,
deadlock-safety and memory-management logic described in Part 1.
