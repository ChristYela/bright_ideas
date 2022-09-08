-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema project_app
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema project_app
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `project_app` DEFAULT CHARACTER SET utf8 ;
USE `project_app` ;

-- -----------------------------------------------------
-- Table `project_app`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project_app`.`users` (
  `users_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `users_password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`users_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `project_app`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project_app`.`posts` (
  `posts_id` INT NOT NULL AUTO_INCREMENT,
  `posts_content` VARCHAR(2550) NOT NULL,
  `post_likes` INT NULL DEFAULT '0',
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`posts_id`),
  INDEX `fk_posts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `project_app`.`users` (`users_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `project_app`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project_app`.`likes` (
  `likes_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  `likes` INT NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`likes_id`),
  INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_likes_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `project_app`.`posts` (`posts_id`),
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `project_app`.`users` (`users_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
