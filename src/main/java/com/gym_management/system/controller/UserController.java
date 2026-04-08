package com.gym_management.system.controller;

import com.gym_management.system.model.dto.CreateUserRequest;
import com.gym_management.system.model.dto.UpdateUserRequest;
import com.gym_management.system.model.dto.UserResponse;
import com.gym_management.system.services.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = "*") // Configurar según necesidades de CORS
@RequiredArgsConstructor
@Slf4j
public class UserController {
    
    private final UserService userService;
    
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
        log.info("POST /api/users - Creando usuario: {}", request.getUsername());
        UserResponse response = userService.createUser(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
    
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        log.info("GET /api/users - Obteniendo todos los usuarios");
        List<UserResponse> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/active")
    public ResponseEntity<List<UserResponse>> getAllActiveUsers() {
        log.info("GET /api/users/active - Obteniendo usuarios activos");
        List<UserResponse> users = userService.getAllActiveUsers();
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        log.info("GET /api/users/{} - Obteniendo usuario por ID", id);
        UserResponse user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/username/{username}")
    public ResponseEntity<UserResponse> getUserByUsername(@PathVariable String username) {
        log.info("GET /api/users/username/{} - Obteniendo usuario por username", username);
        UserResponse user = userService.getUserByUsername(username);
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/email/{email}")
    public ResponseEntity<UserResponse> getUserByEmail(@PathVariable String email) {
        log.info("GET /api/users/email/{} - Obteniendo usuario por email", email);
        UserResponse user = userService.getUserByEmail(email);
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/role/{role}")
    public ResponseEntity<List<UserResponse>> getUsersByRole(@PathVariable String role) {
        log.info("GET /api/users/role/{} - Obteniendo usuarios por rol", role);
        List<UserResponse> users = userService.getUsersByRole(role);
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/role/{role}/active")
    public ResponseEntity<List<UserResponse>> getActiveUsersByRole(@PathVariable String role) {
        log.info("GET /api/users/role/{}/active - Obteniendo usuarios activos por rol", role);
        List<UserResponse> users = userService.getActiveUsersByRole(role);
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/search")
    public ResponseEntity<List<UserResponse>> searchUsers(@RequestParam String q) {
        log.info("GET /api/users/search?q={} - Buscando usuarios", q);
        List<UserResponse> users = userService.searchUsers(q);
        return ResponseEntity.ok(users);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        log.info("PUT /api/users/{} - Actualizando usuario", id);
        UserResponse response = userService.updateUser(id, request);
        return ResponseEntity.ok(response);
    }
    
    @PatchMapping("/{id}/deactivate")
    public ResponseEntity<UserResponse> deactivateUser(@PathVariable Long id) {
        log.info("PATCH /api/users/{}/deactivate - Desactivando usuario", id);
        UserResponse response = userService.deactivateUser(id);
        return ResponseEntity.ok(response);
    }
    
    @PatchMapping("/{id}/activate")
    public ResponseEntity<UserResponse> activateUser(@PathVariable Long id) {
        log.info("PATCH /api/users/{}/activate - Activando usuario", id);
        UserResponse response = userService.activateUser(id);
        return ResponseEntity.ok(response);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        log.info("DELETE /api/users/{} - Eliminando usuario", id);
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
    
    @GetMapping("/exists/username/{username}")
    public ResponseEntity<Boolean> existsByUsername(@PathVariable String username) {
        log.info("GET /api/users/exists/username/{} - Verificando username", username);
        boolean exists = userService.existsByUsername(username);
        return ResponseEntity.ok(exists);
    }
    
    @GetMapping("/exists/email/{email}")
    public ResponseEntity<Boolean> existsByEmail(@PathVariable String email) {
        log.info("GET /api/users/exists/email/{} - Verificando email", email);
        boolean exists = userService.existsByEmail(email);
        return ResponseEntity.ok(exists);
    }

    @GetMapping("/exists/email/{email}/v2")
    public ResponseEntity<Boolean> existsByEmailV2(@PathVariable String email) {
        log.info("GET /api/users/exists/email/{} - Verificando email", email);
        boolean exists = userService.existsByEmail(email);
        return ResponseEntity.ok(exists);
    }


} 