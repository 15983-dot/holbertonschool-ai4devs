import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class UserAuthValidator {
    public static boolean isAdminUser(List<String> roles, String targetRole) {
        if (roles == null || targetRole == null) {
            return false;
        }
        for (String role : roles) {
            if (Objects.equals(role, targetRole)) {
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        List<String> userRoles = Arrays.asList("guest", "editor", null, "admin");
        String requiredRole = new String("admin");

        if (isAdminUser(userRoles, requiredRole)) {
            System.out.println("Access Granted.");
        } else {
            System.out.println("Access Denied.");
        }
    }
}
