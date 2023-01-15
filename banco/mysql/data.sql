-- MySQL Script generated by MySQL Workbench
-- Sun Dec 18 20:35:02 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

-- drop database mydb;
-- drop table cliente;
-- drop table conta_corrente;
-- drop table conta_poupanca;
-- DROP TABLE historico;
-- INSERT INTO historico (momento, tipo, valor, conta_corrente_idconta_corrente) VALUES ('2022-12-27 16:53:02', 'deposito', 150, 1);


SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`cliente` (
  `idcliente` INT UNSIGNED NOT NULL auto_increment,
  `cpf` VARCHAR(11) NOT NULL UNIQUE,
  `nascimento` DATE NOT NULL,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `nome` VARCHAR(100) NOT NULL,
  `senha_acesso` VARCHAR(45) NOT NULL,
  `criacao` DATETIME,
  PRIMARY KEY (`idcliente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`conta_corrente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`conta_corrente` (
  `idconta_corrente` INT NOT NULL AUTO_INCREMENT,
  `numero` VARCHAR(6) NOT NULL UNIQUE,
  `senha` VARCHAR(6) NOT NULL,
  `saldo` FLOAT NULL,
  `limite` FLOAT NOT NULL,
  `criacao` DATETIME,
  `cliente_idcliente` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idconta_corrente`),
    FOREIGN KEY (`cliente_idcliente`)
    REFERENCES `mydb`.`cliente` (`idcliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
SELECT idconta_corrente FROM conta_corrente WHERE numero = 100000;


-- -----------------------------------------------------
-- Table `mydb`.`conta_poupanca`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`conta_poupanca` (
  `idconta_poupanca` INT NOT NULL AUTO_INCREMENT,
  `numero` VARCHAR(6) NOT NULL UNIQUE,
  `senha` VARCHAR(6) NOT NULL,
  `saldo` FLOAT NULL,
  `criacao` DATETIME,
  `cliente_idcliente` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idconta_poupanca`),
    FOREIGN KEY (`cliente_idcliente`)
    REFERENCES `mydb`.`cliente` (`idcliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`historico`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`historico` (
  `idtransacao` INT NOT NULL AUTO_INCREMENT,
  `momento` DATETIME,
  `tipo` VARCHAR(45) ,
  `valor` FLOAT ,
  `conta_poupanca_idconta_poupanca` INT,
  `conta_corrente_idconta_corrente` INT,
  PRIMARY KEY (`idtransacao`),
    FOREIGN KEY (`conta_poupanca_idconta_poupanca`)
    REFERENCES `mydb`.`conta_poupanca` (`idconta_poupanca`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`conta_corrente_idconta_corrente`)
    REFERENCES `mydb`.`conta_corrente` (`idconta_corrente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
