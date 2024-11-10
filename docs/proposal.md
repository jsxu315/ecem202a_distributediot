# Project Proposal

## 1. Motivation & Objective

The goal is to allow home/business owners to be able to quickly have a picture of the activity that goes on inside their buildings, using low-cost/low-power sensors, cameras, and microcontrollers. 

## 2. State of the Art & Its Limitations

Currently, people must individually examine the data for each sensor, and then determine what activities occurred (e.g. check garage and living room cameras to conclude that “a person moved from the garage to the living room”), since each unit would only store its own local, unprocessed data. 

## 3. Novelty & Rationale

We provide classification of data (e.g. “person seen on camera” or “car honk heard”), which reduces the need for users to manually comb over and process sensor data. We create one distributed database, which provides richer insight into the activity that is occurring (e.g. being able to track activity across different areas, or infer cause and effect)

## 4. Potential Impact

For home and business owners, the project can reduce the time and labor needed to determine when certain events occurred in their buildings. This can be useful for ensuring safety or for collecting data about day-to-day usage. 

## 5. Challenges

The main challenges are making accurate classifications and inferences. If our project makes inferences that are wrong (e.g. concluding that a person moved from room A to room B when in fact it was two different people), it could place a burden on the building owners to manually verify the data. Additionally, there is a concern of data privacy when transmitting sensor data between nodes. 

## 6. Requirements for Success

Hardware: 
* Raspberry Pi 5 with AI Hat -- collects sensor data and hosts database (https://www.canakit.com/raspberry-pi-ai-kit.html)
* ReSpeaker 4-Mic Array (https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi.html)
* OV5647 Camera Module (https://www.arducam.com/product/arducam-ov5647-standard-raspberry-pi-camera-b0033/)


Skills/knowledge:
* AI/ML classification 
* Distributed databases 
* Microprocessors, limitations of embedded systems and edge computation 

## 7. Metrics of Success

* Accuracy of classification
* Database availability and uptime 


## 8. Execution Plan

We plan to first set up a minimal network with 2 nodes, each of which collects camera and microphone data, hosts its own local database, and is connected to the other via a wireless LAN. Additionally, they will run Redis Sentinel, which will allow each node to return results from other nodes' databases. 

For ease of development, we plan to separately set up the camera/speaker and database features. Yaqi will set up the camera and speaker functionality on one Raspberry Pi, and Jess will set up the Redis database and connectivity using two other Raspberry Pis. 

Once all parts are functional, we plan to add the classification functionalities and expand the network to ~6 nodes. 


## 9. Related Work

### 9.a. Papers

* **Portkey**[1] is a project that implemenents a distributed edge database using Redis Cluster, with nodes that are mobile (unlike in our project, in which nodes are stationary)  

* **SDKV: A Smart and Distributed Key-Value Store for the Edge-Cloud Continuum**[2] -- this paper also implements a distributed edge database, but it also intelligently determines where to place replicas and allows clients to choose between strong or eventual consistency. This ultimately allows more flexible customization of data availability, consistency, and latency, making it generalizable and scalable. Like Portkey, it uses Redis Cluster. We use ideas from this paper to implement our distributed database, but latency and scalability are not as much of a concern for the scale of our project. 

### 9.b. Datasets

We plan to use the following datasets: 

* For sound classification: ESC-50: Dataset for Environmental Sound Classification [3]

* For image classification: COCO (Common Objects in Context) [4]

### 9.c. Software

* Redis Sentinel [5] 
* Node-RED server [6]
 

## 10. References

1. Joseph Noor, Mani Srivastava, and Ravi Netravali. 2021. Portkey: Adaptive Key-Value Placement over Dynamic Edge Networks. In Proceedings of the ACM Symposium on Cloud Computing (SoCC '21). Association for Computing Machinery, New York, NY, USA, 197–213. https://doi.org/10.1145/3472883.3487004 

2. Juan Aznar-Poveda, Tobias Pockstaller, Thomas Fahringer, Stefan Pedratscher, and Zahra Najafabadi Samani. 2024. SDKV: A Smart and Distributed Key-Value Store for the Edge-Cloud Continuum. In Proceedings of the IEEE/ACM 16th International Conference on Utility and Cloud Computing (UCC '23). Association for Computing Machinery, New York, NY, USA, Article 2, 1–8. https://doi.org/10.1145/3603166.3632126 

3. ESC-50: Dataset for Environmental Sound Classification (https://github.com/karolpiczak/ESC-50) 

4. COCO (Common Objects in Context) (https://cocodataset.org/#home) 

5. Redis Sentinel (https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)

6. Node-RED (https://nodered.org/) 