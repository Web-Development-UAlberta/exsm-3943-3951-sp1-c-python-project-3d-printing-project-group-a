import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Login Page", () => {
  it("renders the login page", () => {
    render(
      <div>
        <h1>Welcome back</h1>
        <input placeholder="Enter your username" />
        <input placeholder="Enter your password" />
        <button>Sign in</button>
      </div>,
    );

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
