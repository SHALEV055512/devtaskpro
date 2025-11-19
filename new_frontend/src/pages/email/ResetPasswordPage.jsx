import { useState } from "react";
import {
  Box,
  Text,
  Heading,
  Button,
  Input,
  VStack,
  useToast,
  InputGroup,
  InputRightElement,
  IconButton,
} from "@chakra-ui/react";

import { Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function ResetPasswordPage() {
  // -------------------------------------------------------
  // State Management
  // -------------------------------------------------------
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [showPassword1, setShowPassword1] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);
  const [loading, setLoading] = useState(false);

  const toast = useToast();
  const navigate = useNavigate();

  // Retrieve stored email from previous step
  const email = localStorage.getItem("resetEmail");

  // -------------------------------------------------------
  // Handle password reset flow
  // -------------------------------------------------------
  const handleReset = async () => {
    // Validate matching passwords
    if (password !== password2) {
      toast({
        title: "Passwords do not match",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    // Validate token
    if (!token.trim()) {
      toast({
        title: "Missing Code",
        description: "Please enter the reset code.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      setLoading(true);

      // Step 1: Verify reset code
      const verifyRes = await fetch("http://localhost:5000/api/verify_reset_token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, token }),
      });

      const verifyData = await verifyRes.json();
      if (!verifyRes.ok) throw new Error(verifyData.message);

      // Step 2: Perform password reset
      const resetRes = await fetch("http://localhost:5000/api/reset_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });

      const resetData = await resetRes.json();
      if (!resetRes.ok) throw new Error(resetData.message);

      // Success feedback
      toast({
        title: "Password updated!",
        description: "Redirecting to login...",
        status: "success",
        duration: 2500,
        isClosable: true,
      });

      localStorage.removeItem("resetEmail");
      setTimeout(() => navigate("/login"), 2000);

    } catch (err) {
      toast({
        title: "Error",
        description: err.message,
        status: "error",
        duration: 3500,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  // -------------------------------------------------------
  // UI Layout
  // -------------------------------------------------------
  return (
    <Box
      height="100vh"
      display="flex"
      justifyContent="center"
      alignItems="center"
      /* Unified radial gradient for all auth pages */
      bgGradient={`radial-gradient(circle at 50% 80%, 
        rgba(80, 130, 255, 0.9) 40%, 
        rgba(144, 206, 245, 0.9) 60%,
        rgb(255, 255, 255) 70%
      )`}
    >
      {/* Main Glass Card */}
      <Box
        bg="rgba(255, 255, 255, 0.22)"
        backdropFilter="blur(18px)"
        borderRadius="16px"
        boxShadow="0 8px 40px rgba(0, 0, 0, 0.25)"
        border="1px solid rgba(255, 255, 255, 0.30)"
        p={20}
        textAlign="center"
        color="white"
        maxW="720px"
        w="92%"
      >
        {/* Page Title */}
        <Heading size="3xl" mb={8}>
          Reset Password
        </Heading>

        {/* Subtext */}
        <Text fontSize="xl" mb={10} opacity={0.95}>
          Enter the code you received and choose a new password.
        </Text>

        {/* Form Section */}
        <VStack spacing={6}>

          {/* Reset Code */}
          <Input
            placeholder="Reset code"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            textAlign="center"
            fontSize="lg"
            height="56px"
            bg="white"
            border="1px solid #d0d7e2"
            borderRadius="10px"
            color="black"
            _placeholder={{ color: "#888" }}
            _focus={{
              borderColor: "#3b82f6",
              boxShadow: "0 0 0 2px rgba(59,130,246,0.3)",
            }}
          />

          {/* New Password */}
          <InputGroup>
            <Input
              placeholder="New password"
              type={showPassword1 ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              textAlign="center"
              fontSize="lg"
              height="56px"
              bg="white"
              border="1px solid #d0d7e2"
              borderRadius="10px"
              color="black"
              _placeholder={{ color: "#888" }}
              _focus={{
                borderColor: "#3b82f6",
                boxShadow: "0 0 0 2px rgba(59,130,246,0.3)",
              }}
              pr="60px"
            />
            <InputRightElement height="100%" pr="18px">
              <IconButton
                aria-label="Toggle password visibility"
                icon={showPassword1 ? <Eye size={24} /> : <EyeOff size={24} />}
                size="sm"
                variant="ghost"
                onClick={() => setShowPassword1((prev) => !prev)}
                _hover={{ bg: "transparent" }}
                _active={{ bg: "transparent" }}
                color="black"
              />
            </InputRightElement>
          </InputGroup>

          {/* Confirm Password */}
          <InputGroup>
            <Input
              placeholder="Confirm password"
              type={showPassword2 ? "text" : "password"}
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              textAlign="center"
              fontSize="lg"
              height="56px"
              bg="white"
              border="1px solid #d0d7e2"
              borderRadius="10px"
              color="black"
              _placeholder={{ color: "#888" }}
              _focus={{
                borderColor: "#3b82f6",
                boxShadow: "0 0 0 2px rgba(59,130,246,0.3)",
              }}
              pr="60px"
            />
            <InputRightElement height="100%" pr="18px">
              <IconButton
                aria-label="Toggle password visibility"
                icon={showPassword2 ? <Eye size={24} /> : <EyeOff size={24} />}
                size="sm"
                variant="ghost"
                onClick={() => setShowPassword2((prev) => !prev)}
                _hover={{ bg: "transparent" }}
                _active={{ bg: "transparent" }}
                color="black"
              />
            </InputRightElement>
          </InputGroup>

          {/* Submit Button */}
          <Button
            colorScheme="blue"
            size="lg"
            height="58px"
            fontSize="lg"
            width="100%"
            borderRadius="full"
            onClick={handleReset}
            isLoading={loading}
            boxShadow="0 6px 20px rgba(0,0,0,0.5)"
            _hover={{
              transform: "scale(1.06)",
              transition: "0.25s",
              bg: "blue.600",
            }}
          >
            Reset Password
          </Button>
        </VStack>
      </Box>
    </Box>
  );
}
