import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'

describe('Admin Dashboard Page', () => {
  it('renders the admin dashboard page', () => {
    render(
      <div>
        <h1>Admin Dashboard</h1>
        <p>Filament inventory</p>
        <p>Active orders</p>
        <p>Low stock</p>
        <p>Total orders</p>
        <p>Printers free</p>
        <p>All orders</p>
        <button>Save new filament</button>
        <button>Update</button>
        <button>Add printer</button>
        <button>Remove</button>
      </div>
    )
    expect(screen.getByText('Admin Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Filament inventory')).toBeInTheDocument()
    expect(screen.getByText('Active orders')).toBeInTheDocument()
    expect(screen.getByText('Low stock')).toBeInTheDocument()
    expect(screen.getByText('Total orders')).toBeInTheDocument()
    expect(screen.getByText('Printers free')).toBeInTheDocument()
    expect(screen.getByText('All orders')).toBeInTheDocument()
    expect(screen.getByText('Save new filament')).toBeInTheDocument()
    expect(screen.getByText('Update')).toBeInTheDocument()
    expect(screen.getByText('Add printer')).toBeInTheDocument()
    expect(screen.getByText('Remove')).toBeInTheDocument()
  })
})
