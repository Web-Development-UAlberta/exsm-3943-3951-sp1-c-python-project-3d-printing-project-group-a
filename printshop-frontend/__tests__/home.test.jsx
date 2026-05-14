import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import Home from "../app/page";

describe("Home Page", () => {
  it("renders the home page", () => {
    render(<Home />);
    expect(screen.getByText("Browse by category")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Search models...")).toBeInTheDocument();
    expect(screen.getByText("Model library")).toBeInTheDocument();
    expect(screen.getByText("Desk Vase")).toBeInTheDocument();
  });
});
