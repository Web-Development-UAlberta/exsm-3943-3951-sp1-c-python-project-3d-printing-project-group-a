import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import ProfilePage from "../app/profile/page";

describe("Profile Page", () => {
  it("renders the profile page", () => {
    render(<ProfilePage />);
    expect(screen.getByText("My profile")).toBeInTheDocument();
    expect(screen.getByText("My orders")).toBeInTheDocument();
    expect(screen.getByText("Edit profile")).toBeInTheDocument();
    expect(screen.getByText("View all orders")).toBeInTheDocument();
  });
});
