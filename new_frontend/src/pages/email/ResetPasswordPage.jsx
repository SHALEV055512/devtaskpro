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
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [showPassword1, setShowPassword1] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);
  const [loading, setLoading] = useState(false);

  const toast = useToast();
  const navigate = useNavigate();

  // ✅ האימייל מהשלב הקודם
  const email = localStorage.getItem("resetEmail");

  const handleReset = async () => {
    if (password !== password2) {
      toast({
        title: "Passwords do not match",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

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

      // ✅ אימות טוקן
      const verifyRes = await fetch("http://localhost:5000/api/verify_reset_token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, token }),
      });
      const verifyData = await verifyRes.json();
      if (!verifyRes.ok) throw new Error(verifyData.message);

      // ✅ איפוס ססמה
      const resetRes = await fetch("http://localhost:5000/api/reset_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({password}),
      });
      const resetData = await resetRes.json();
      if (!resetRes.ok) throw new Error(resetData.message);

      toast({
        title: "✅ Password updated!",
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

  return (
    <Box
      height="100vh"
      display="flex"
      justifyContent="center"
      alignItems="center"
      bgGradient="linear(to-br, blue.700, cyan.300)"
    >
      <Box
        bg="rgba(255, 255, 255, 0.28)"
        backdropFilter="blur(22px)"
        borderRadius="2xl"
        boxShadow="0 18px 70px rgba(0,0,0,0.45)"
        border="1px solid rgba(255,255,255,0.35)"
        p={20}
        textAlign="center"
        color="white"
        maxW="650px"
        w="92%"
      >
        <Heading size="3xl" mb={8}>
          Reset Password
        </Heading>

        <Text fontSize="xl" mb={10} opacity={0.95}>
          Enter the code you received and choose a new password.
        </Text>

        <VStack spacing={6}>
          {/* ✅ Reset Code */}
          <Input
            placeholder="Reset code"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            textAlign="center"
            fontSize="lg"
            height="58px"
            bg="rgba(255,255,255,0.35)"
            border="2px solid rgba(255,255,255,0.55)"
            color="white"
            _placeholder={{ color: "whiteAlpha.800", fontSize: "lg" }}
            _focus={{ borderColor: "white", boxShadow: "0 0 0 2px white" }}
          />

                   {/* ✅ New Password with Eye (Chakra InputGroup) */}
          <InputGroup>
            <Input
              placeholder="New password"
              type={showPassword1 ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              textAlign="center"
              fontSize="lg"
              height="58px"
              bg="rgba(255,255,255,0.35)"
              border="2px solid rgba(255,255,255,0.55)"
              color="white"
              _placeholder={{ color: "whiteAlpha.800", fontSize: "lg" }}
              _focus={{ borderColor: "white", boxShadow: "0 0 0 2px white" }}
              pr="60px" // שיהיה רווח לטקסט מהעין
            />

            <InputRightElement height="100%" pr="18px">
              <IconButton
                aria-label={showPassword1 ? "Hide password" : "Show password"}
                icon={showPassword1 ? <Eye size={24} /> : <EyeOff size={24} />}
                size="sm"
                variant="ghost"
                onClick={() => setShowPassword1((prev) => !prev)}
                _hover={{ bg: "transparent" }}
                _active={{ bg: "transparent" }}
                color="white"
              />
            </InputRightElement>
          </InputGroup>


                   {/* ✅ Confirm Password with Eye */}
          <InputGroup>
            <Input
              placeholder="Confirm password"
              type={showPassword2 ? "text" : "password"}
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              textAlign="center"
              fontSize="lg"
              height="58px"
              bg="rgba(255,255,255,0.35)"
              border="2px solid rgba(255,255,255,0.55)"
              color="white"
              _placeholder={{ color: "whiteAlpha.800", fontSize: "lg" }}
              _focus={{ borderColor: "white", boxShadow: "0 0 0 2px white" }}
              pr="60px"
            />

            <InputRightElement height="100%" pr="18px">
              <IconButton
                aria-label={showPassword2 ? "Hide password" : "Show password"}
                icon={showPassword2 ? <Eye size={24} /> : <EyeOff size={24} />}
                size="sm"
                variant="ghost"
                onClick={() => setShowPassword2((prev) => !prev)}
                _hover={{ bg: "transparent" }}
                _active={{ bg: "transparent" }}
                color="white"
              />
            </InputRightElement>
          </InputGroup>


          {/* ✅ Button */}
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
