import { useState } from "react";
import {
  Box,
  Text,
  Heading,
  Button,
  Input,
  VStack,
  useToast,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

export default function ForgotPasswordPage() {
  // -------------------------------------------------------
  // State Management
  // -------------------------------------------------------
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const toast = useToast();
  const navigate = useNavigate();

  // -------------------------------------------------------
  // Handle sending reset request
  // -------------------------------------------------------
  const handleSend = async () => {
    // Validate email input
    if (!email.trim()) {
      toast({
        title: "Missing Email",
        description: "Please enter your email address.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      setLoading(true);

      // Send request to backend
      const res = await fetch("http://localhost:5000/api/forgot_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      // Display backend response in toast
      toast({
        title: data.message || "Unknown response",
        status: res.ok ? "success" : "error",
        duration: 4000,
        isClosable: true,
      });

      // If successful → store email + navigate to reset page
      if (res.ok) {
        localStorage.setItem("resetEmail", email);
        navigate("/reset_password");
      }
    } catch (err) {
      // Network or unexpected error
      toast({
        title: "Something went wrong",
        description: "Please try again later.",
        status: "error",
        duration: 4000,
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
      bgGradient={`radial-gradient(circle at 50% 80%, 
        rgba(80, 130, 255, 0.9) 40%, 
        rgba(144, 206, 245, 0.9) 60%,
        rgb(255, 255, 255) 70%
      )`}
    >
      {/* Glass effect main container */}
      <Box
        bg="rgba(255, 255, 255, 0.22)"
        backdropFilter="blur(18px)"
        borderRadius="16px"
        boxShadow="0 8px 40px rgba(0, 0, 0, 0.25)"
        border="1px solid rgba(255, 255, 255, 0.30)"
        p={12}
        textAlign="center"
        color="white"
        maxW="720px"
        w="90%"
        minH="420px"
      >
        {/* Page Title */}
        <Heading size="3xl" mb={8}>
          Forgot Password
        </Heading>

        {/* Sub text */}
        <Text fontSize="xl" mb={12} opacity={0.95}>
          Enter your email and we’ll send you a reset code.
        </Text>

        {/* Form Section */}
        <VStack spacing={6}>
          {/* Email Input */}
          <Input
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            textAlign="left"
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
            w="100%"
          />

          {/* Submit Button */}
          <Button
            colorScheme="blue"
            size="lg"
            height="58px"
            fontSize="lg"
            width="100%"
            borderRadius="full"
            onClick={handleSend}
            isLoading={loading}
            boxShadow="0 6px 20px rgba(0,0,0,0.5)"
            _hover={{
              transform: "scale(1.06)",
              transition: "0.25s",
              bg: "blue.600",
            }}
          >
            Send Reset Code
          </Button>

          {/* Back to Login — text clickable */}
          <Text
            width="100%"
            textAlign="center"
            fontSize="1rem"
            fontWeight="700"
            color="#000"
            cursor="pointer"
            _hover={{ color: "gray.500" }}
            onClick={() => navigate("/login")}
          >
            Back to Login
          </Text>
        </VStack>
      </Box>
    </Box>
  );
}
