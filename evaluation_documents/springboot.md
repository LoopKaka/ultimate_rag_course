# Spring Boot

## What Is Spring Boot?

Spring Boot is an open-source Java framework designed to simplify the development of standalone, production-grade applications.

It was created by VMware as an extension of the Spring Framework. Spring Boot follows the **convention over configuration** principle, reducing the need for complex XML configuration and manual setup.

## Auto-Configuration

Spring Boot automatically configures an application based on the dependencies available in the project.

For example, when you add the appropriate web starter dependency, Spring Boot configures many of the components required to build a web application.

This reduces boilerplate configuration and helps developers get started quickly.

## Embedded Servers

Spring Boot supports embedded web servers, allowing applications to run without requiring a separately installed application server.

Common embedded server options include:

- **Tomcat**
- **Jetty**
- **Undertow**

For example, a Spring Boot web application can start its embedded server when the application runs.

## Starter Dependencies

Spring Boot provides starter dependencies that simplify dependency management.

For example, `spring-boot-starter-web` provides commonly used dependencies for building web applications and REST APIs.

Instead of manually adding multiple related libraries, developers can use a starter dependency to bring in the required components.

## Production-Ready Features

Spring Boot provides features that help developers build and operate production applications.

These include:

- Application health monitoring.
- Metrics and monitoring integration.
- Externalized configuration.
- Support for application management through Spring Boot Actuator.

These features make it easier to monitor and configure applications across different environments.

## Configuration Without XML

Spring Boot reduces the need for XML-based configuration.

Developers can configure applications using Java annotations, Java configuration classes, and properties or YAML files.

For example, application settings can be maintained in `application.properties` or `application.yml`.

## Summary

Spring Boot simplifies Java application development through auto-configuration, starter dependencies, embedded servers, and production-ready features. It reduces boilerplate configuration and helps developers build standalone, production-grade applications more efficiently.
