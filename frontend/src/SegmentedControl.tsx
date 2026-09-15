interface Option {
  value: number
  label: string
}

interface Props {
  options: Option[]
  value: number
  onChange: (value: number) => void
}

export default function SegmentedControl({ options, value, onChange }: Props) {
  return (
    <div className="segmented" role="radiogroup">
      {options.map((opt) => (
        <button
          type="button"
          key={opt.value}
          role="radio"
          aria-checked={opt.value === value}
          className={opt.value === value ? 'segment selected' : 'segment'}
          onClick={() => onChange(opt.value)}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}
