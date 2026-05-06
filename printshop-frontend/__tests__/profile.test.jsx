import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'

describe('Profile Page', () => {
  it('renders the profile page', () => {
    render(
      <div>
        <h1>My profile</h1>
        <p>My orders</p>
        <button>Edit profile</button>
        <button>View all orders</button>
        <button>Cancel</button>
      </div>
    )
    expect(screen.getByText('My profile')).toBeInTheDocument()
    expect(screen.getByText('My orders')).toBeInTheDocument()
    expect(screen.getByText('Edit profile')).toBeInTheDocument()
    expect(screen.getByText('View all orders')).toBeInTheDocument()
    expect(screen.getByText('Cancel')).toBeInTheDocument()
  })
})
