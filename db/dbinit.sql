CREATE DATABASE Webstore;
USE Webstore;
CREATE TABLE user
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username NVARCHAR(70) NOT NULL UNIQUE,
	password NVARCHAR(150) NOT NULL,
	type INT NOT NULL DEFAULT 0,
	CHECK (type>=0),
	CHECK (type<=2)
);

CREATE TABLE offer
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	owner INT NOT NULL,
	name NVARCHAR(300) NOT NULL,
	description NVARCHAR(10000) NOT NULL DEFAULT '',
	price DECIMAL(15,2) UNSIGNED NOT NULL,
	qty INT NOT NULL DEFAULT 0,
	sold INT NOT NULL DEFAULT 0,
	FOREIGN KEY (owner) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE cartitem
(
	offer INT NOT NULL,
	owner INT NOT NULL,
	qty INT NOT NULL DEFAULT 1,
	PRIMARY KEY (offer,owner),
	FOREIGN KEY (offer) REFERENCES offer(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (owner) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER //
CREATE TRIGGER limit_listings
BEFORE INSERT ON offer
FOR EACH ROW
BEGIN
 IF (SELECT COUNT(*) FROM offer WHERE offer.owner = new.owner GROUP BY offer.owner) >= 10 THEN
  SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO=30001, MESSAGE_TEXT='Vendor reached offer limit';
 END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE commitCart(IN ownerid INT)
BEGIN
 DECLARE done INT DEFAULT FALSE;
 DECLARE success INT DEFAULT TRUE;
 DECLARE cowner INT;
 DECLARE coffer INT;
 DECLARE cqty INT;
 DECLARE oqty INT;
 DECLARE osold INT;
 DECLARE cur1 CURSOR FOR SELECT cartitem.offer, cartitem.owner, cartitem.qty, offer.qty, offer.sold FROM cartitem JOIN offer ON cartitem.offer=offer.id;
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
 
 OPEN cur1;
 START TRANSACTION;
 WHILE NOT done AND success DO
  FETCH cur1 INTO coffer, cowner, cqty, oqty, osold;
  IF NOT done THEN
   IF cqty <= oqty THEN
    UPDATE offer SET qty = (oqty - cqty) WHERE id = coffer;
    UPDATE offer SET sold = (osold + cqty) WHERE id = coffer;
    DELETE FROM cartitem WHERE offer = coffer AND owner = cowner;
   ELSE
    SET success = FALSE;
   END IF;
  END IF;
 END WHILE;
 
 IF success THEN
  COMMIT;
 ELSE
  ROLLBACK;
  SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO=30002, MESSAGE_TEXT='Not enough supply in stock';
 END IF;
 
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE searchProc(IN query NVARCHAR(400))
BEGIN
EXECUTE searchStmt USING query;
END; //
DELIMITER ;

PREPARE searchStmt FROM
'SELECT name,price,owner,id FROM offer WHERE name LIKE ''%'' || ? || ''%'' ';

INSERT INTO user (username, password, type) VALUES ("admin", "pbkdf2:sha256:150000$deadbeef", 2);

CREATE USER 'authusr' IDENTIFIED BY 'verysecure';
CREATE USER 'shopusr' IDENTIFIED BY 'buyconsume';

GRANT SELECT,INSERT,DELETE,UPDATE ON Webstore.user TO 'authusr';
GRANT SELECT (id,username,type) ON Webstore.user TO 'shopusr';
GRANT SELECT,INSERT,DELETE,UPDATE,TRIGGER ON Webstore.offer TO 'shopusr';
GRANT EXECUTE ON PROCEDURE Webstore.searchProc TO 'shopusr';
GRANT EXECUTE ON PROCEDURE Webstore.commitCart TO 'shopusr';
GRANT SELECT,INSERT,DELETE,UPDATE ON Webstore.cartitem TO 'shopusr';



