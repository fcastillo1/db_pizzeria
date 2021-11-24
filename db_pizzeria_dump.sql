-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_pizzeria
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_pizzeria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_pizzeria` DEFAULT CHARACTER SET utf8 ;
USE `db_pizzeria` ;

-- -----------------------------------------------------
-- Table `db_pizzeria`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`cliente` (
  `rut_cli` VARCHAR(9) NOT NULL,
  `nom_clie` VARCHAR(200) NOT NULL,
  `ape_clie` VARCHAR(200) NOT NULL,
  `tel_clie` INT NOT NULL,
  `dir_clie` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`rut_cli`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`tipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`tipo` (
  `id_tipo` INT NOT NULL,
  `nom_tipo` VARCHAR(200) NOT NULL,
  `capacidad_tipo` INT NOT NULL,
  PRIMARY KEY (`id_tipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`vehiculo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`vehiculo` (
  `id_patente` VARCHAR(10) NOT NULL,
  `id_tipo` INT NOT NULL,
  PRIMARY KEY (`id_patente`),
  INDEX `fk_vehiculo_tipo1_idx` (`id_tipo` ASC) VISIBLE,
  CONSTRAINT `fk_vehiculo_tipo1`
    FOREIGN KEY (`id_tipo`)
    REFERENCES `db_pizzeria`.`tipo` (`id_tipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`repartidor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`repartidor` (
  `rut_rep` VARCHAR(9) NOT NULL,
  `nom_rep` VARCHAR(200) NOT NULL,
  `ape_rep` VARCHAR(200) NOT NULL,
  `tel_rep` INT NOT NULL,
  `id_patente` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`rut_rep`),
  INDEX `fk_repartidor_vehiculo1_idx` (`id_patente` ASC) VISIBLE,
  CONSTRAINT `fk_repartidor_vehiculo1`
    FOREIGN KEY (`id_patente`)
    REFERENCES `db_pizzeria`.`vehiculo` (`id_patente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`pedido` (
  `id_pedido` INT NOT NULL,
  `total_pedido` INT NOT NULL,
  `fecha_pedido` DATETIME NOT NULL,
  `fecha_reparto` DATETIME NOT NULL,
  `rut_cli` VARCHAR(9) NOT NULL,
  `rut_rep` VARCHAR(9) NOT NULL,
  PRIMARY KEY (`id_pedido`),
  INDEX `fk_pedido_cliente1_idx` (`rut_cli` ASC) VISIBLE,
  INDEX `fk_pedido_repartidor1_idx` (`rut_rep` ASC) VISIBLE,
  CONSTRAINT `fk_pedido_cliente1`
    FOREIGN KEY (`rut_cli`)
    REFERENCES `db_pizzeria`.`cliente` (`rut_cli`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_repartidor1`
    FOREIGN KEY (`rut_rep`)
    REFERENCES `db_pizzeria`.`repartidor` (`rut_rep`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`tamano`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`tamano` (
  `id_tam` INT NOT NULL,
  `nom_tam` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id_tam`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`pizza`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`pizza` (
  `id_piz` INT NOT NULL,
  `nom_piz` VARCHAR(200) NOT NULL,
  `precio_pizz` INT NOT NULL,
  `id_tam` INT NOT NULL,
  PRIMARY KEY (`id_piz`),
  INDEX `fk_pizza_tamano1_idx` (`id_tam` ASC) VISIBLE,
  CONSTRAINT `fk_pizza_tamano1`
    FOREIGN KEY (`id_tam`)
    REFERENCES `db_pizzeria`.`tamano` (`id_tam`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_pizzeria`.`pedido_has_pizza`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_pizzeria`.`pedido_has_pizza` (
  `id_pedido` INT NOT NULL,
  `id_piz` INT NOT NULL,
  `cantidad` INT NOT NULL,
  `precio` INT NOT NULL,
  PRIMARY KEY (`id_pedido`, `id_piz`),
  INDEX `fk_pedido_has_pizza_pizza1_idx` (`id_piz` ASC) VISIBLE,
  INDEX `fk_pedido_has_pizza_pedido1_idx` (`id_pedido` ASC) VISIBLE,
  CONSTRAINT `fk_pedido_has_pizza_pedido1`
    FOREIGN KEY (`id_pedido`)
    REFERENCES `db_pizzeria`.`pedido` (`id_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_has_pizza_pizza1`
    FOREIGN KEY (`id_piz`)
    REFERENCES `db_pizzeria`.`pizza` (`id_piz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
