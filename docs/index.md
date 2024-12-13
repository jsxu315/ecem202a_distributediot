# Abstract

The goal of our project is to allow home and business owners to be able to quickly gain an overview of the activity that occurs inside a given building or building complex, using low-cost/low-power sensors, cameras, and microcontrollers. To this end, a highly available distributed database is needed, as well as accurate classification of sound and images. 

Each node in our network consists of a Raspberry Pi with a camera and microphone that hosts a Redis vector database. Each entry contains a vector embedding and classification of an event, and nodes in the network are connected via a wireless LAN, using Redis Sentinel to provide a highly available distributed database. 

Results: TBD

# Team

* Yaqi Liu
* Jess Xu

# Required Submissions

* [Proposal](proposal)
* [Midterm Checkpoint Presentation Slides](https://docs.google.com/presentation/d/1FnyzDtgjOtIwzm3ZAPmfm1_xH2ywoqEGA7hYzbvL638/edit?usp=sharing)
* [Final Presentation Slides](https://docs.google.com/presentation/d/16QAUWB5lgkDse2qqXDBuBWtdzMkf59NhxkH5aq5M7S8/edit#slide=id.p1)
* [Final Report](report)
