import React from 'react'
import { passwordGenerator } from "../../../app/passGenerator";
import Switch from "react-switch";
import { UseFormSetValue } from 'react-hook-form';
import { IPassword } from 'app/api/setPassword';

/**
 * generate password options
 *
 * @export
 * @param {{ setValue: UseFormSetValue<IPassword> }} { setValue } - react hook form set value
 * @returns {React.ReactElement} - react element
 */
export default function genPassOptions(
    { setValue }: { setValue: UseFormSetValue<IPassword> },
): React.ReactElement {
    const [isUpperCase, setIsUpperCase] = React.useState<boolean>(false);
    const [isLowerCase, setIsLowerCase] = React.useState<boolean>(false);
    const [isNumbers, setIsNumbers] = React.useState<boolean>(false);
    const [isSymbols, setIsSymbols] = React.useState<boolean>(false);
    const [passLength, setPassLength] = React.useState<number>(8);

    return (
        <div className="lg:grid lg:grid-rows-2 sm:flex sm:flex-col lg:grid-flow-col gap-4 rounded-md shadow-md p-4 mt-5">
            <label>
                <span className="block">With capital letters</span>
                <Switch
                onChange={(checked) => setIsUpperCase(checked)}
                checked={isUpperCase}
                />
            </label>
            <label>
                <span className="block">With small letters</span>
                <Switch
                onChange={(checked) => setIsLowerCase(checked)}
                checked={isLowerCase}
                />
            </label>
            <label>
                <span className="block">With numbers</span>
                <Switch
                onChange={(checked) => setIsNumbers(checked)}
                checked={isNumbers}
                />
            </label>
            <label>
                <span className="block">With symbols</span>
                <Switch
                    onChange={(checked) => setIsSymbols(checked)}
                    checked={isSymbols}
                />
            </label>
            <label>
                <span className="block">Password length</span>
                <input
                className="form-input w-full mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400
                focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500
                disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
                invalid:border-pink-500 invalid:text-pink-600
                focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                type="number"
                min="8"
                max="32"
                value={passLength}
                onChange={(e) => setPassLength(parseInt(e.target.value))}
                />
            </label>
            <button
                className="w-full rounded-full bg-secondary text-black font-semibold py-2 px-4 mt-4 hover:border-black hover:border-2 cursor-pointer hover:bg-white hover:text-secondary transition duration-500 ease-in-out"
                type='button'
                onClick={() => {
                    setValue("password", passwordGenerator({
                        is_lowercase: isLowerCase,
                        is_uppercase: isUpperCase,
                        is_number: isNumbers,
                        is_special: isSymbols,
                        length: passLength,
                    }));
                }}
            >
                Generate
            </button>
            </div>
    )
}