import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Edit Profile Page", () => {
  it("renders the edit profile page", () => {
    render(
      <div>
        <h1>Edit your profile</h1>
        <p>Personal details</p>
        <input placeholder="Roel_M" />
        <input placeholder="Robel Measho" />
        <input
          placeholder="japan@em.com
        "
        />
        <input placeholder="780-890-4711" />
        <p>Change password</p>
        <input placeholder="Enter current password" />
        <input placeholder="Min 8 chars" />
        <p>Saved payment details</p>
        <button>Update saved card</button>
        <button>Save changes</button>
        <button>Cancel</button>
      </div>,
    );

    expect(screen.getByText("Edit your profile")).toBeInTheDocument();
    expect(screen.getByText("Personal details")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Roel_M")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Robel Measho")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("japan@em.com")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("780-890-4711")).toBeInTheDocument();
    expect(screen.getByText("Change password")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Enter current password"),
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Min 8 chars")).toBeInTheDocument();
    expect(screen.getByText("Saved payment details")).toBeInTheDocument();
    expect(screen.getByText("Update saved card")).toBeInTheDocument();
    expect(screen.getByText("Save changes")).toBeInTheDocument();
    expect(screen.getByText("Cancel")).toBeInTheDocument();
  });
});
