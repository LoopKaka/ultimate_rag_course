# Angular Developer Guide

Angular is a TypeScript-based framework for building modern web applications.

Angular provides features such as components, dependency injection, routing,
forms, HTTP communication, reactive programming, state management,
change detection, and lazy loading.

This guide contains practical Angular concepts, APIs, configuration examples,
error codes, and common development scenarios.

---

# 1. Angular Components

Components are the basic building blocks of an Angular application.

A component normally contains:

- TypeScript class
- HTML template
- CSS styles
- Component metadata

Example:

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-user",
  template: ` <h1>{{ name }}</h1> `,
})
export class UserComponent {
  name = "John";
}
```

The `@Component` decorator tells Angular that the class is an Angular component.

The `selector` defines the HTML element used to render the component.

For example:

```html
<app-user></app-user>
```

---

# 2. Angular Dependency Injection

Dependency Injection is one of the core concepts in Angular.

It allows Angular to create and provide objects that a component or service
depends on.

Instead of creating dependencies manually using the `new` keyword, Angular's
dependency injection system can create the required object and provide it
automatically.

Example:

```typescript
import { Component } from "@angular/core";
import { UserService } from "./user.service";

@Component({
  selector: "app-user",
  template: `<h1>User</h1>`,
})
export class UserComponent {
  constructor(private userService: UserService) {}
}
```

In this example, `UserComponent` depends on `UserService`.

Angular creates the service and injects it into the component.

Modern Angular also supports the `inject()` function.

Example:

```typescript
import { Component, inject } from "@angular/core";
import { UserService } from "./user.service";

@Component({
  selector: "app-user",
  template: `<h1>User</h1>`,
})
export class UserComponent {
  private userService = inject(UserService);
}
```

---

# 3. Angular Services

Services are commonly used to contain reusable business logic and communicate
with backend APIs.

Example:

```typescript
import { Injectable } from "@angular/core";

@Injectable({
  providedIn: "root",
})
export class UserService {
  getUsers() {
    return [];
  }
}
```

The `@Injectable` decorator tells Angular that a class can participate in
dependency injection.

The following configuration:

```typescript
@Injectable({
  providedIn: 'root'
})
```

registers the service with the root injector.

Using `providedIn: 'root'` makes the service available throughout the
application through Angular's dependency injection system.

---

# 4. Angular Standalone Components

Angular supports standalone components.

A standalone component can be used without declaring it inside an NgModule.

Example:

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-dashboard",
  standalone: true,
  template: ` <h1>Dashboard</h1> `,
})
export class DashboardComponent {}
```

The `standalone: true` property indicates that the component is standalone.

Standalone components can directly import the dependencies they need.

---

# 5. Angular Signals

Signals provide a reactive way to manage state.

Example:

```typescript
import { signal } from '@angular/core';

count = signal(0);

increment() {
  this.count.update(value => value + 1);
}
```

The current signal value can be read using:

```typescript
count();
```

The value can be replaced using:

```typescript
count.set(10);
```

A signal can also be updated based on its previous value:

```typescript
count.update((value) => value + 1);
```

Angular also provides `computed()` for derived state.

Example:

```typescript
import { computed, signal } from "@angular/core";

count = signal(10);

doubleCount = computed(() => this.count() * 2);
```

---

# 6. Angular Routing

Angular Router provides navigation between different views of an application.

Example:

```typescript
import { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "home",
    component: HomeComponent,
  },
  {
    path: "users",
    component: UsersComponent,
  },
];
```

Navigation can be performed from an Angular template using:

```html
<a routerLink="/users"> Users </a>
```

Programmatic navigation can be performed using:

```typescript
this.router.navigate(["/users"]);
```

---

# 7. Lazy Loading

Lazy loading allows Angular to load application features only when they are
required.

Instead of loading every feature when the application starts, Angular can
load a feature when the user navigates to it.

Example:

```typescript
export const routes: Routes = [
  {
    path: "admin",
    loadComponent: () =>
      import("./admin/admin.component").then((m) => m.AdminComponent),
  },
];
```

Lazy loading can reduce the initial JavaScript bundle and improve application
startup performance.

---

# 8. Angular HTTP Client

Angular provides `HttpClient` for communicating with backend APIs.

Example:

```typescript
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
  providedIn: "root",
})
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers() {
    return this.http.get("/api/users");
  }
}
```

The HTTP request returns an Observable.

Example:

```typescript
this.userService.getUsers().subscribe((users) => {
  console.log(users);
});
```

The `HttpClient` can be used to perform GET, POST, PUT, PATCH, and DELETE
requests.

---

# 9. HTTP Interceptors

HTTP interceptors can inspect or modify HTTP requests and responses.

They are commonly used for:

- Adding authentication tokens
- Logging requests
- Handling common errors
- Adding HTTP headers
- Processing responses

Example:

```typescript
import { HttpInterceptorFn } from "@angular/common/http";

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authReq = req.clone({
    setHeaders: {
      Authorization: "Bearer TOKEN",
    },
  });

  return next(authReq);
};
```

The `HttpInterceptorFn` type is used for functional HTTP interceptors.

An interceptor is useful when the same HTTP behavior needs to be applied
to many API requests.

---

# 10. Reactive Forms

Angular Reactive Forms provide a programmatic approach to managing form state
and validation.

Example:

```typescript
import { FormControl, FormGroup } from "@angular/forms";

userForm = new FormGroup({
  name: new FormControl(""),
  email: new FormControl(""),
});
```

The form can be connected to an Angular template:

```html
<form [formGroup]="userForm">
  <input formControlName="name" />

  <input formControlName="email" />

  <button type="submit">Save</button>
</form>
```

Reactive Forms are useful when forms contain complex validation rules or
dynamic controls.

---

# 11. Form Validation

Angular provides built-in validators.

Example:

```typescript
import { FormControl, Validators } from "@angular/forms";

email = new FormControl("", [Validators.required, Validators.email]);
```

Common validators include:

```text
Validators.required
Validators.email
Validators.minLength
Validators.maxLength
Validators.pattern
```

Validators allow an application to check whether user input satisfies
specific requirements.

---

# 12. RxJS Observables

Angular uses RxJS extensively for asynchronous operations.

An Observable represents a stream of values over time.

Example:

```typescript
import { Observable } from "rxjs";

const users$: Observable<User[]> = this.userService.getUsers();
```

RxJS provides operators that can transform, filter, combine, and control
asynchronous data streams.

Common operators include:

```text
map()
filter()
switchMap()
catchError()
debounceTime()
```

---

# 13. switchMap and Search

`switchMap` is useful when implementing search functionality.

Consider a search box where the user enters text continuously.

Every change in the search box could trigger an API request.

Example:

```typescript
searchControl.valueChanges
  .pipe(
    debounceTime(300),
    switchMap((query) => this.userService.searchUsers(query)),
  )
  .subscribe((users) => {
    this.users = users;
  });
```

`debounceTime(300)` waits until the user stops typing for a short period.

`switchMap()` switches to the latest search request.

This pattern is commonly used to implement search-as-you-type functionality.

---

# 14. Angular Change Detection

Change detection is the mechanism Angular uses to detect changes in application
state and update the user interface.

Angular provides different change detection strategies.

One important strategy is:

```typescript
ChangeDetectionStrategy.OnPush;
```

Example:

```typescript
import { ChangeDetectionStrategy, Component } from "@angular/core";

@Component({
  selector: "app-user",
  template: `<p>{{ name }}</p>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserComponent {
  name = "John";
}
```

The `OnPush` strategy can reduce unnecessary change detection work when the
application is designed appropriately.

It is commonly used when developers want more predictable and efficient
change detection behavior.

---

# 15. Angular Lifecycle Hooks

Angular components have a lifecycle.

Angular provides lifecycle hooks that allow developers to execute logic
at specific stages of the component lifecycle.

Common lifecycle hooks include:

```text
ngOnInit()
ngOnChanges()
ngAfterViewInit()
ngOnDestroy()
```

Example:

```typescript
import { Component, OnInit } from "@angular/core";

@Component({
  selector: "app-user",
  template: `<p>User</p>`,
})
export class UserComponent implements OnInit {
  ngOnInit() {
    console.log("Component initialized");
  }
}
```

`ngOnInit()` is commonly used to perform initialization logic after Angular
has initialized the component.

---

# 16. Angular Authentication

Angular applications commonly communicate with authenticated backend APIs.

An HTTP interceptor can add an authentication token to outgoing requests.

Example:

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authReq = req.clone({
    setHeaders: {
      Authorization: "Bearer TOKEN",
    },
  });

  return next(authReq);
};
```

This approach allows authentication-related request logic to be centralized
instead of manually adding the token in every service method.

---

# 17. Angular Performance Optimization

Angular applications can be optimized using several techniques.

Common approaches include:

- Lazy loading
- OnPush change detection
- Avoiding unnecessary computations in templates
- Efficient list rendering
- Reducing unnecessary HTTP requests
- Using appropriate RxJS operators

Lazy loading can reduce the initial bundle size.

`ChangeDetectionStrategy.OnPush` can reduce unnecessary change detection work.

RxJS operators such as `debounceTime()` can reduce the number of API requests
generated by rapidly changing user input.

---

# 18. Angular Error NG8001

Angular error `NG8001` occurs when Angular does not recognize an element
used inside a template.

Example:

```text
NG8001: 'app-user' is not a known element
```

Possible causes include:

- The component is not imported.
- The selector is incorrect.
- A standalone component is missing from the imports.
- A component is not declared correctly in a module-based application.

For example, if the template contains:

```html
<app-user></app-user>
```

but Angular cannot find the component associated with the `app-user` selector,
Angular can report error `NG8001`.

---

# 19. Angular Error NG0100

Angular error `NG0100` is:

```text
ExpressionChangedAfterItHasBeenCheckedError
```

This error can occur when a bound value changes after Angular has already
checked the value during a change detection cycle.

The error is commonly investigated by looking at the component lifecycle,
change detection, and code that changes bound values during initialization.

---

# 20. Angular API Reference

Important Angular APIs and concepts covered in this guide include:

```text
@Component
@Injectable
inject()
signal()
computed()
Routes
routerLink
HttpClient
HttpInterceptorFn
FormControl
FormGroup
Validators.required
Validators.email
Validators.minLength
Observable
switchMap()
debounceTime()
ChangeDetectionStrategy.OnPush
ngOnInit()
ngOnDestroy()
NG8001
NG0100
```

These APIs and identifiers are commonly encountered when developing
Angular applications.
