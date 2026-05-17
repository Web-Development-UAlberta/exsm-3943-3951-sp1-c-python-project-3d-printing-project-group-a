import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import EditProfilePage from "../app/profile/edit/page";

jest.mock("../app/lib/api", () => ({
  apiGet: jest.fn(),
  apiPut: jest.fn(),
}));

describe("Edit Profile Page", () => {
  it("renders the edit profile page", () => {
    render(<EditProfilePage />);
    expect(screen.getByText("Loading profile...")).toBeInTheDocument();
  });
});
