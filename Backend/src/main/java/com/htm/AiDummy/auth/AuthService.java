package com.htm.AiDummy.auth;

import com.htm.AiDummy.auth.dto.AuthResponse;
import com.htm.AiDummy.auth.dto.LoginRequest;
import com.htm.AiDummy.auth.dto.SignupRequest;
import com.htm.AiDummy.auth.dto.UserResponse;
import com.htm.AiDummy.security.CustomUserDetails;
import com.htm.AiDummy.security.JwtTokenProvider;
import com.htm.AiDummy.user.User;
import com.htm.AiDummy.user.UserRepository;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            AuthenticationManager authenticationManager,
            JwtTokenProvider jwtTokenProvider
    ) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Transactional
    public UserResponse signup(SignupRequest request) {
        if (userRepository.existsByUserName(request.userName())) {
            throw new IllegalArgumentException("이미 사용 중인 userName 입니다.");
        }

        User user = new User(
                request.userName(),
                passwordEncoder.encode(request.password()),
                request.displayName()
        );

        User savedUser = userRepository.save(user);
        return new UserResponse(savedUser.getId(), savedUser.getUserName(), savedUser.getDisplayName());
    }

    public AuthResponse login(LoginRequest request) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.userName(), request.password())
            );

            CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
            String accessToken = jwtTokenProvider.createToken(authentication);

            return new AuthResponse(
                    accessToken,
                    "Bearer",
                    userDetails.getUsername(),
                    userDetails.getDisplayName()
            );
        } catch (BadCredentialsException ex) {
            throw new IllegalArgumentException("아이디 또는 비밀번호가 올바르지 않습니다.");
        }
    }
}
