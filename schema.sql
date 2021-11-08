drop table if exists tickets;

create table tickets (
    APP_NM text not null,
    TICKET integer primary key,
    RESOLUTION text not null,
    TICKET_TYPE text not null,
    COMMENT text not null,
    CREATED_ON text not null,--timestamp DATE not null default (datetime ('now', 'localtime'))
    MON text not null
)