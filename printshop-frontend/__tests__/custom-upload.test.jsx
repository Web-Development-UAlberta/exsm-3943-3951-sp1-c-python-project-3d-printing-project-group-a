import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import CustomUploadPage from "../app/custom/page";

describe("Custom Upload Page", () => {
  it("renders the custom upload page", () => {
    render(<CustomUploadPage />);
    expect(
      screen.getByText(/upload your custom 3d model/i),
    ).toBeInTheDocument();
    expect(screen.getByText("Upload file")).toBeInTheDocument();
    expect(screen.getByText("Step 1 — Upload")).toBeInTheDocument();
  });
});
