import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Home Page", () => {
  it("renders the page", () => {
    render(
      <div>
        <h1>PrintShop</h1>
      </div>,
    );
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
  });
});
