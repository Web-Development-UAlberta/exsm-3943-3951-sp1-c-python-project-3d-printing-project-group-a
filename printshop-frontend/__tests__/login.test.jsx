import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import LoginPage from "../app/login/page";

describe("Login Page", () => {
  it("renders the login page", () => {
    render(<LoginPage />);
    expect(screen.getByText("Welcome back")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Enter your username"),
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Enter your password"),
    ).toBeInTheDocument();
    expect(screen.getByText("Sign in")).toBeInTheDocument();
  });
});
