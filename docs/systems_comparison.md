## Traditional FL Systems 

```bash
+------------+     +------------+     +------------+
|            |     |            |     |            |
|   Client   +---->+   Client   +---->+   Client   |
|   Model 1  |     |   Model 2  |     |   Model 3  |
|            |     |            |     |            |
+------+-----+     +-----+------+     +-----+------+
       |                 |                  |
       |                 |                  |
       v                 v                  v
    +--+-----------------+------------------+--+
    |                                          |
    |             Central Aggregation          |
    |                Server (FL)               |
    |                                          |
    +--+-----------------+------------------+--+
       |                 |                  |
       |                 |                  |
       v                 v                  v
+------+-+          +---+---+          +----+---+
|         |          |       |          |        |
|  Client  |          | Client |          | Client  |
|  Model 1 |          | Model 2|          | Model 3 |
|         |          |       |          |        |
+---------+          +-------+          +--------+

```

----


## Blockchain enhanced FL Systems

```bash
 +------------+    +------------+     +------------+
|            |     |            |     |            |
|   Client   +---->+   Client   +---->+   Client   |
|   Model 1  |     |   Model 2  |     |   Model 3  |
|            |     |            |     |            |
+------+-----+     +-----+------+     +-----+------+
       |                 |                  |
       |   (Secure and   |                  |
       |   Encrypted     |   (Secure and    |
       |   Transactions) |   Encrypted      |
       |                 |   Transactions)  |
       v                 v                  v
+------+-----------------+-----------------+------+
|                                                 |
|             Blockchain Network                  |
|         (Distributed Ledger & Smart Contracts)  |
|                                                 |
+------+-----------------+-----------------+------+
       |                 |                  |
       |                 |                  |
       |   (Model        |                  |
       |   Updates and   |   (Model         |
       |   Aggregations) |   Updates and    |
       v                 v   Aggregations)  v
+------+-+          +---+---+          +----+---+
|         |          |       |          |        |
|  Client  |         | Client |         | Client |
|  Model 1 |         | Model 2|         | Model 3|
|         |          |       |          |        |
+---------+          +-------+          +--------+

```