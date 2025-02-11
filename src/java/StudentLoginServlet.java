import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;




@WebServlet("/StudentLogin")
public class StudentLoginServlet extends HttpServlet {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/clg_port";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "0721";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.sendRedirect("StudentLogin.jsp");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        HttpSession session = request.getSession();

        String studentId = request.getParameter("student_id");

        try {
            // Load MySQL JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // Establish Connection
            try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
                // Query to verify the student ID
                String query = "SELECT name FROM student WHERE student_id = ?";
                PreparedStatement pstmt = conn.prepareStatement(query);
                pstmt.setString(1, studentId);

                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    // If student ID is found in the database
                    String name = rs.getString("name");
                    session.setAttribute("student_id", studentId);
                    session.setAttribute("student_name", name);
                    response.sendRedirect("student.html");
                } else {
                    // If student ID is invalid
                    session.setAttribute("errorMessage", "Invalid Student ID. Please try again.");
                    response.sendRedirect("StudentLogin.jsp");
                }
            }
        } catch (ClassNotFoundException | SQLException e) {
            // Handle database or driver errors
            e.printStackTrace();
            session.setAttribute("errorMessage", "An error occurred. Please try again later.");
            response.sendRedirect("StudentLogin.jsp");
        }
    }
}

