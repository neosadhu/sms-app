CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, message_id VARCHAR(255), 
message_content VARCHAR(255),timestamp TIMESTAMP DEFAULT current_timestamp);