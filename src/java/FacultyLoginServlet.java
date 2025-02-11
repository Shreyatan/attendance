import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;


@WebServlet("/FacultyLogin")
public class FacultyLoginServlet extends HttpServlet {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/clg_port";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "0721";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.sendRedirect("FacultyLogin.jsp");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        HttpSession session = request.getSession();

        String facultyId = request.getParameter("faculty_id");
        String password = request.getParameter("password");

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
                String query = "SELECT name FROM faculty WHERE faculty_id = ? AND password = ?";
                PreparedStatement pstmt = conn.prepareStatement(query);
                pstmt.setString(1, facultyId);
                pstmt.setString(2, password);

                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    String name = rs.getString("name");
                    session.setAttribute("faculty_id", facultyId);
                    session.setAttribute("faculty_name", name);
                    response.sendRedirect("faculty.html");
                } else {
                    session.setAttribute("errorMessage", "Invalid faculty ID or password. Please try again.");
                    response.sendRedirect("FacultyLogin.jsp");
                }
            }
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
            session.setAttribute("errorMessage", "An error occurred. Please try again later.");
            response.sendRedirect("FacultyLogin.jsp");
        }
    }
}
