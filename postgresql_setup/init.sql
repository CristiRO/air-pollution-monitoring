CREATE TABLE users(
    id          serial primary key,
    username    varchar(40) not null,
    pass        varchar(40) not null
);

CREATE TABLE sensors(
    sensor_id       serial primary key,
    owner_id        int references users(id),
    sensor_lat      float not null,
    sensor_long     float not null
);

CREATE TABLE sensor_data(
    sensor_id       int references sensors(sensor_id),
    measure_ts      timestamp not null,
    measure_type    varchar(40) not null,
    measure_value   float not null
);

insert into users(username, pass) values
    ('IDP2020', 'DOCKER_RULES');
insert into sensors(owner_id, sensor_lat, sensor_long) values
    ((SELECT id from users WHERE username='IDP2020'), 44.426765, 26.102537)
