import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import ProfilePage from "../app/profile/page";

describe("Profile Page", () => {
  it("renders the profile page", () => {
    render(<ProfilePage />);
    expect(screen.getByText("Loading profile...")).toBeInTheDocument();
  });
});
