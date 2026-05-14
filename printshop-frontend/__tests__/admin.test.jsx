import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import AdminPage from "../app/admin/page";

describe("Admin Dashboard Page", () => {
  it("renders the admin dashboard page", () => {
    render(<AdminPage />);
    expect(screen.getByText("Admin Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Filament inventory")).toBeInTheDocument();
    expect(screen.getByText("User management")).toBeInTheDocument();
    expect(screen.getByText("All orders")).toBeInTheDocument();
    expect(screen.getByText("+ Add printer")).toBeInTheDocument();
  });
});
