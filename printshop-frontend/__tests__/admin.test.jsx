import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import AdminPage from "../app/admin/page";

describe("Admin Dashboard Page", () => {
  it("renders the admin dashboard page", () => {
    render(<AdminPage />);
    expect(screen.getByText("Loading dashboard...")).toBeInTheDocument();
  });
});
