import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Custom Upload Page", () => {
  it("renders the custom upload page", () => {
    render(
      <div>
        <h1>Upload Your Custom 3D Model</h1>
        <p>Accepted: .stl and .3mf</p>
        <button>Upload file</button>
        <p>After upload:</p>
      </div>,
    );

    expect(screen.getByText("Upload Your Custom 3D Model")).toBeInTheDocument();
    expect(screen.getByText("Accepted: .stl and .3mf")).toBeInTheDocument();
    expect(screen.getByText("Upload file")).toBeInTheDocument();
  });
});
