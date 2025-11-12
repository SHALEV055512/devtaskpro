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
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const handleSend = async () => {
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

      // ✅ כתובת נכונה לאיפוס ססמה
      const res = await fetch("http://localhost:5000/api/forgot_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      await res.json(); // לא חשוב מה תוכן התשובה - UX ניטרלי

      toast({
        title: "If the email exists, a reset code has been sent.",
        status: "info",
        duration: 4000,
        isClosable: true,
      });

      // ✅ שומרים את המייל לשלב הבא
      localStorage.setItem("resetEmail", email);

      // ✅ מעבר למסך הזנת טוקן וססמה חדשה
      navigate("/reset_password");

    } catch (err) {
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

 return (
  <Box
    height="100vh"
    display="flex"
    justifyContent="center"
    alignItems="center"
    bgGradient="linear(to-br, blue.700, cyan.300)"  // כהה יותר
  >
    <Box
      bg="rgba(255, 255, 255, 0.28)"                // כהה יחסית
      backdropFilter="blur(22px)"                   // טשטוש עמוק יותר
      borderRadius="2xl"
      boxShadow="0 18px 70px rgba(0, 0, 0, 0.45)"   // צל חזק
      border="1px solid rgba(255, 255, 255, 0.35)"
      p={20}                                        // ✅ הרבה יותר גדול
      textAlign="center"
      color="white"
      maxW="650px"                                  // ✅ ריבוע רחב
      w="92%"
    >
      <Heading size="3xl" mb={8}>
        Forgot Password
      </Heading>

      <Text fontSize="xl" mb={12} opacity={0.95}>
        Enter your email and we’ll send you a reset code.
      </Text>

      <VStack spacing={6}>
        <Input
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          textAlign="center"
          fontSize="lg"
          height="58px"
          bg="rgba(255,255,255,0.35)"
          border="2px solid rgba(255,255,255,0.55)"
          color="white"
          _placeholder={{ color: "whiteAlpha.800", fontSize: "lg" }}
          _focus={{ borderColor: "white", boxShadow: "0 0 0 2px white" }}
          dir="ltr"
        />

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

        <Button
          variant="ghost"
          fontSize="md"
          color="whiteAlpha.900"
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
