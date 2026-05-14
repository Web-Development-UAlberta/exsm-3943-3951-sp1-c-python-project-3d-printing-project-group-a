import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import EditProfilePage from "../app/profile/edit/page";

describe("Edit Profile Page", () => {
  it("renders the edit profile page", () => {
    render(<EditProfilePage />);
    expect(screen.getByText("Edit your profile")).toBeInTheDocument();
    expect(screen.getByText("Personal details")).toBeInTheDocument();
    expect(screen.getByText("Change password")).toBeInTheDocument();
    expect(screen.getByText("Saved payment details")).toBeInTheDocument();
    expect(screen.getByText("Save changes")).toBeInTheDocument();
  });
});
