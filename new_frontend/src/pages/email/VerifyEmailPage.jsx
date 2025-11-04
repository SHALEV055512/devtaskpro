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

export default function VerifyEmailPage() {
  const [token, setToken] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  // 📧 כתובת המייל נשמרה אחרי ההרשמה
  const email = localStorage.getItem("pendingEmail") || "";

  const handleVerify = async () => {
    if (!token) {
      toast({
        title: "Missing Code",
        description: "Please enter the 6-digit verification code.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      setLoading(true);
      const res = await fetch("http://localhost:5000/api/verify_email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, token }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Verification failed");

      toast({
        title: "✅ Email Verified!",
        description: "Your account has been successfully created.",
        status: "success",
        duration: 4000,
        isClosable: true,
      });

      localStorage.removeItem("pendingEmail");
      navigate("/login");
    } catch (err) {
      toast({
        title: "❌ Verification Failed",
        description: err.message || "Invalid or expired token.",
        status: "error",
        duration: 4000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      height="100vh"
      display="flex"
      justifyContent="center"
      alignItems="center"
      bgGradient="linear(to-br, blue.500, cyan.100)"
    >
      <Box
        bg="rgba(255, 255, 255, 0.18)"
        backdropFilter="blur(12px)"
        borderRadius="2xl"
        boxShadow="0 8px 40px rgba(0, 0, 0, 0.25)"
        border="1px solid rgba(255, 255, 255, 0.3)"
        p={14}
        textAlign="center"
        color="white"
        maxW="480px"
        w="90%"
      >
        <Heading size="2xl" mb={5}>
          Verify Your Email
        </Heading>

        <Text fontSize="lg" mb={8} opacity={0.9}>
          We sent a 6-digit verification code to:{" "}
          <strong style={{ color: "#fff" }}>{email}</strong>
        </Text>

        <VStack spacing={4}>
          <Input
            placeholder="Enter verification code"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            textAlign="center"
            fontSize="xl"
            letterSpacing="4px"
            bg="rgba(255,255,255,0.2)"
            border="1px solid rgba(255,255,255,0.4)"
            color="white"
            _placeholder={{ color: "whiteAlpha.700" }}
            _focus={{ borderColor: "white", boxShadow: "0 0 0 1px white" }}
          />

          <Button
            colorScheme="blue"
            size="lg"
            width="100%"
            borderRadius="full"
            onClick={handleVerify}
            isLoading={loading}
            boxShadow="0 4px 12px rgba(0,0,0,0.3)"
            _hover={{
              transform: "scale(1.05)",
              transition: "0.2s",
              bg: "blue.600",
            }}
          >
            Verify Email
          </Button>

          <Button
            variant="ghost"
            color="whiteAlpha.800"
            _hover={{ textDecoration: "underline" }}
            onClick={() => navigate("/login")}
          >
            Back to Login
          </Button>
        </VStack>
      </Box>
    </Box>
  );
}
