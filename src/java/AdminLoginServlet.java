import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;




@WebServlet("/AdminLogin")
public class AdminLoginServlet extends HttpServlet {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/clg_port";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "0721";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.sendRedirect("AdminLogin.jsp");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        HttpSession session = request.getSession();

        // Get admin ID and password from request
        String adminId = request.getParameter("admin_id");
        String password = request.getParameter("password");

        try {
            // Load MySQL JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // Establish database connection
            try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
                // SQL query to check credentials
                String query = "SELECT name FROM admin WHERE admin_id = ? AND password = ?";
                PreparedStatement pstmt = conn.prepareStatement(query);
                pstmt.setString(1, adminId);
                pstmt.setString(2, password);

                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    // If admin ID and password match
                    String name = rs.getString("name");
                    session.setAttribute("admin_id", adminId);
                    session.setAttribute("admin_name", name);
                    response.sendRedirect("admin.html"); // Redirect to admin dashboard
                } else {
                    // If credentials are invalid
                    session.setAttribute("errorMessage", "Invalid Admin ID or Password. Please try again.");
                    response.sendRedirect("AdminLogin.jsp"); // Redirect back to login page
                }
            }
        } catch (ClassNotFoundException | SQLException e) {
            // Handle errors
            e.printStackTrace();
            session.setAttribute("errorMessage", "An error occurred. Please try again later.");
            response.sendRedirect("AdminLogin.jsp"); // Redirect back to login page
        }
    }
}

