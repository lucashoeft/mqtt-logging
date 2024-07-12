CREATE TABLE mqtt_logs (
    mqtt_id                 serial primary key,
    mqtt_log                TEXT,
    mqtt_local_datetime     TIMESTAMPTZ,
    mqtt_topic              TEXT,
    mqtt_content            JSONB,
    mqtt_field_timestamp    TIMESTAMPTZ,
    mqtt_field_order_id      TEXT,
    mqtt_field_parameters   TEXT,
    mqtt_field_fault_type    TEXT,
    mqtt_field_fault_active  TEXT
);