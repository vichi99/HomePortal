import React from 'react'


interface Props {
    name: string
    value: number | undefined
    unit: string | undefined
}

const ValueLine = (props: Props) => {
    const { name, value, unit } = props
    return (
        <div>
            { value === undefined ? (null) :
                (
                    <div className="actualData">
                        <p>{name}: <b>
                            {value} {unit}</b>
                        </p>
                    </div>
                )
            }
        </div>
    )
}

export default ValueLine
