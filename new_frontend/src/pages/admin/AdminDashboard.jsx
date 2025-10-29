import { Box, Text, Heading, Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const handleLogout = () => {
    navigate("/login"); 
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
          Admin Dashboard
        </Heading>

        <Text fontSize="xl" mb={8} opacity={0.95}>
          You are logged in as <strong>Admin</strong>
        </Text>

        <Button
          colorScheme="blue"
          size="lg"
          borderRadius="full"
          px={10}
          onClick={handleLogout}
          boxShadow="0 4px 12px rgba(0,0,0,0.3)"
          _hover={{ transform: "scale(1.05)", transition: "0.2s" }}
        >
          Log out
        </Button>
      </Box>
    </Box>
  );
}
