CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE content.restaurant (
    id UUID PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC'
);

CREATE TABLE content.table_type (
    id UUID PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    seats INTEGER NOT NULL CHECK (seats >= 1),
    description TEXT,
    price_per_seat DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    restaurant_id UUID NOT NULL,
    CONSTRAINT fk_tabletype_restaurant FOREIGN KEY (restaurant_id) 
        REFERENCES content.restaurant(id) ON DELETE CASCADE
);

CREATE TABLE content.menu_item (
    id UUID PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date DATE NOT NULL,
    course VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    allergens JSONB NOT NULL DEFAULT '[]'::jsonb,
    restaurant_id UUID NOT NULL,
    CONSTRAINT fk_menuitem_restaurant FOREIGN KEY (restaurant_id) 
        REFERENCES content.restaurant(id) ON DELETE CASCADE
);

CREATE TABLE content.reservation (
    id UUID PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date DATE NOT NULL,
    time TIME WITHOUT TIME ZONE NOT NULL,
    party_size INTEGER NOT NULL CHECK (party_size >= 1),
    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    restaurant_id UUID NOT NULL,
    table_type_id UUID NOT NULL,
    CONSTRAINT fk_reservation_restaurant FOREIGN KEY (restaurant_id) 
        REFERENCES content.restaurant(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservation_tabletype FOREIGN KEY (table_type_id) 
        REFERENCES content.table_type(id) ON DELETE CASCADE
);

CREATE TABLE content.reservation_guest (
    id UUID PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(254),
    notes TEXT,
    reservation_id UUID NOT NULL,
    CONSTRAINT fk_reservationguest_reservation FOREIGN KEY (reservation_id) 
        REFERENCES content.reservation(id) ON DELETE CASCADE
);

CREATE INDEX idx_tabletype_restaurant ON content.table_type(restaurant_id);
CREATE INDEX idx_menuitem_restaurant ON content.menu_item(restaurant_id);
CREATE INDEX idx_reservation_restaurant ON content.reservation(restaurant_id);
CREATE INDEX idx_reservation_tabletype ON content.reservation(table_type_id);
CREATE INDEX idx_reservationguest_reservation ON content.reservation_guest(reservation_id);