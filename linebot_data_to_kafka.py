import sys
from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaException, KafkaError


# 用來接收從 Consumer instance 發出的 error 訊息
def error_callback(err):
    sys.stderr.write(f'Error: {err}')

# 轉換 msg_key 或 msg_value 成為 utf-8 的字串
def try_decode_utf8(data):
    return data.decode('utf-8') if data else None

# 指定要從哪個 partition, offset 開始讀資料
def my_assign(consumer_instance, partitions):
    for p in partitions:
        p.offset = 0

    print(f'assign: {partitions}')
    consumer_instance.assign(partitions)

def linebot_kafka_producer(user_id, info_data):
    # 步驟1. 設定要連線到 Kafka 集群的相關設定
    props = {
        # Kafka 集群在那裡?
        'bootstrap.servers': 'localhost:9092',    # <-- 置換成要連接的 Kafka 集群
        'error_cb': error_callback                # 設定接收 error 訊息的 callback 函數
    }

    # 步驟2. 產生一個 Kafka 的 Producer 的實例
    producer = Producer(props)

    # 步驟3. 指定想要發佈訊息的 topic 名稱
    topic_name = 'test3'

    try:
        info_data = str(info_data)
        producer.produce(topic=topic_name, key=user_id,value=info_data)
        producer.flush()

        check_kafka_producer = print(f'Send {info_data} to Kafka')

        return check_kafka_producer
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write(
            f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again\n'
        )

    except Exception as e:
        sys.stderr.write(str(e))

    finally:
        # 步驟5. 確認所在 Buffer 的訊息都己經送出去給 Kafka 了
        producer.flush(5)

def linebot_kafka_consumer():
    # 步驟1.設定要連線到 Kafka 集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': 'localhost:9092',  # Kafka 集群在那裡? (置換成要連接的 Kafka 集群)
        'group.id': 'STUDENT_ID',  # ConsumerGroup 的名稱 (置換成你/妳的學員 ID)
        'auto.offset.reset': 'earliest',  # Offset 從最前面開始
        'session.timeout.ms': 6000,  # consumer超過6000ms沒有與 kafka 連線，會被認為掛掉了
        'error_cb': error_callback  # 設定接收 error 訊息的 callback 函數
    }
    # 步驟2. 產生一個 Kafka 的 Consumer 的實例
    consumer = Consumer(props)

    # 步驟3. 指定想要訂閱訊息的 topic 名稱
    topic_name = "test3"

    # 步驟4. 讓 Consumer 向 Kafka 集群訂閱指定的 topic
    consumer.subscribe([topic_name], on_assign=my_assign)

    # 步驟5. 持續的拉取 Kafka 有進來的訊息
    try:
        while True:
            # 請求 Kafka 把新的訊息吐出來
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取

            if not records:
                continue

            for record in records:
                if not record:
                    continue

                # 檢查是否有錯誤
                if record.error() and record.error().code() != KafkaError._PARTITION_EOF:
                    raise KafkaException(record.error())

                else:
                    # ** 在這裡進行商業邏輯與訊息處理 **

                    # 取出相關的 metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()

                    # 取出 msg_key 與 msg_value
                    msg_key = try_decode_utf8(record.key())
                    msg_value = try_decode_utf8(record.value())

                    # 秀出 metadata 與 msg_key & msg_value 訊息
                    check_kafka_consumer = ('{}-{}-{} : ({} , {})'.format(
                        topic, partition, offset, msg_key, msg_value)
                    )

                    return consumer, check_kafka_consumer

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')

    except Exception as e:
        sys.stderr.write(str(e))
    #
    # finally:
    #     # 步驟6.關掉 Consumer 實例的連線
    #     consumer.close()


