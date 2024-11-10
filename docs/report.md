# Table of Contents
* Abstract
* [Introduction](#1-introduction)
* [Related Work](#2-related-work)
* [Technical Approach](#3-technical-approach)
* [Evaluation and Results](#4-evaluation-and-results)
* [Discussion and Conclusions](#5-discussion-and-conclusions)
* [References](#6-references)

# Abstract

The goal of our project is to allow home and business owners to be able to quickly gain an overview of the activity that occurs inside a given building or building complex, using low-cost/low-power sensors, cameras, and microcontrollers. To this end, a highly available distributed database is needed, as well as accurate classification of sound and images. 

Each node in our network consists of a Raspberry Pi with a camera and microphone that hosts a Redis vector database. Each entry contains a vector embedding and classification of an event, and nodes in the network are connected via a wireless LAN, using Redis Cluster to provide a highly available distributed database. 

Results: TBD

# 1. Introduction


Currently, people must individually examine the data for each sensor, and then determine what activities occurred (e.g. check garage and living room cameras to conclude that “a person moved from the garage to the living room”), since each unit would only store its own local, unprocessed data. 

We provide classification of data (e.g. “person seen on camera” or “car honk heard”), which reduces the need for users to manually comb over and process sensor data. We create one distributed database, which provides richer insight into the activity that is occurring (e.g. being able to track activity across different areas, or infer cause and effect)

For home and business owners, the project can reduce the time and labor needed to determine when certain events occurred in their buildings. This can be useful for ensuring safety or for collecting data about day-to-day usage. 

The main challenges are making accurate classifications and inferences. If our project makes inferences that are wrong (e.g. concluding that a person moved from room A to room B when in fact it was two different people), it could place a burden on the building owners to manually verify the data. Additionally, there is a concern of data privacy when transmitting sensor data between nodes. 

Each node in our project requires a Raspberry Pi 5 with AI Hat (to collect and process sensor data and host its database), a ReSpeaker 4-Mic Array, and a OV5647 Camera Module. Executing it will require knowledge of AI/ML classification; distributed databases; microprocessors, and limitations of embedded systems and edge computation. 

We measure the success of our project by the availability (uptime %) of our database, as well as the accuracy of classifications. 


# 2. Related Work

* **Portkey**[1] is a project that implemenents a distributed edge database using Redis Cluster, with nodes that are mobile (unlike in our project, in which nodes are stationary)  

* **SDKV: A Smart and Distributed Key-Value Store for the Edge-Cloud Continuum**[2] -- this paper also implements a distributed edge database, but it also intelligently determines where to place replicas and allows clients to choose between strong or eventual consistency. This ultimately allows more flexible customization of data availability, consistency, and latency, making it generalizable and scalable. Like Portkey, it uses Redis Cluster. We use ideas from this paper to implement our distributed database, but latency and scalability are not as much of a concern for the scale of our project. 

# 3. Technical Approach

We plan to first set up a minimal network with 2 nodes, each of which collects camera and microphone data, hosts its own local database, and is connected to the other via a wireless LAN. Additionally, they will run Redis Sentinel, which will allow each node to return results from other nodes' databases. 

For ease of development, we plan to separately set up the camera/speaker and database features. Yaqi will set up the camera and speaker functionality on one Raspberry Pi, and Jess will set up the Redis database and connectivity using two other Raspberry Pis. 

Once all parts are functional, we plan to add the classification functionalities and expand the network to ~6 nodes. 

# 4. Evaluation and Results

We currently have the ReSpeaker set up to collect audio on a Raspberry Pi, and a Redis vector database set up on the other Pis. 

# 5. Discussion and Conclusions

* TBD 

# 6. References

1. Joseph Noor, Mani Srivastava, and Ravi Netravali. 2021. Portkey: Adaptive Key-Value Placement over Dynamic Edge Networks. In Proceedings of the ACM Symposium on Cloud Computing (SoCC '21). Association for Computing Machinery, New York, NY, USA, 197–213. https://doi.org/10.1145/3472883.3487004 

2. Juan Aznar-Poveda, Tobias Pockstaller, Thomas Fahringer, Stefan Pedratscher, and Zahra Najafabadi Samani. 2024. SDKV: A Smart and Distributed Key-Value Store for the Edge-Cloud Continuum. In Proceedings of the IEEE/ACM 16th International Conference on Utility and Cloud Computing (UCC '23). Association for Computing Machinery, New York, NY, USA, Article 2, 1–8. https://doi.org/10.1145/3603166.3632126 
