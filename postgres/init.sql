CREATE TABLE mqtt_logs (
    mqtt_id                 serial primary key,
    mqtt_log                TEXT,
    mqtt_local_datetime     TIMESTAMPTZ,
    mqtt_topic              TEXT,
    mqtt_content            JSONB
);