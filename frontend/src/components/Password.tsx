import React from 'react';
import { requestPassword } from '../../app/api/requestPassword';
import config from 'src/server/config';
import Swal from 'sweetalert2';

interface IPasswordProps {
    id: string;
}

/**
 * password component to display password
 *
 * @export - password component
 * @param {IPasswordProps} { id } - id of password
 * @returns {React.ReactElement} - password component
 */
export default function Password({ id }: IPasswordProps) : React.ReactElement {

    // Set loading state to true
    const [loading, setLoading] = React.useState<boolean>(true);

    // Set password to empty string
    const [password, setPassword] = React.useState<string>("");

    // Set expTime to empty string
    const [expTime, setExpTime] = React.useState<string | number>("");

    if(password === "" && loading) {
        requestPassword(id, config.app.API_URL).then((res) => {
            setLoading(false);
            setPassword(res.password);
            if(res.valid_until)
                setExpTime(res.valid_until);
        }).catch((err) => {
            setLoading(false);
        }).finally(() => {
            setLoading(false);
        });
    }
    return (
        <div className="relative px-7 py-7 gap-5 max-w-md mx-auto bg-white shadow-md rounded-xl shadow-lg flex justify-center items-center space-x-4">
            <div className="shrink-0 w-1/4">
                <img 
                    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAADEUlEQVR4nO2bzUtUURjGfxgoFQWV00K3FaT9CbWocZeSGea/UJRGGX2sikKy8i9oHS7aBrWIUoqoIDCqhVFtAt1mM1FpyI0Dz4WDnTsz1/nw3I8HXrjnPc87c97nfN65dyBHjvWgHRgBpoF54KdsXr6T4qQSJ4CvQFDFvgBDpAibgCkrwffAOaAX2Crrle+DxbsLtJECTCmhP8DpKkkZsc4Ay4q5QwqGfaDkD8vXAYwBr601wFyPqs7giCXCIAlFuzXnT8nXDbyrMP/nxDE4K9/npC6MI9acb1Pvhsl/0+jYJhvUThCK0KHp8FG+YRKIaTXeLG5o2IfJ73Twd6guUO8bnFf5PgnEJzW+R+U3Kpuej8KwOK9UPqCyGR2JQ0mNN0PcoLym7MJ2cUws4trlRCGQRZUbHecdFtTwg8AhXRtfZgSYdGxzt7IkQLtEWJBN1rifp0aAODDC3AYWa7hZimtxxPdqugQNtlqm34ZhsQUCmO/wFkGLzFsEuQDkIyDIpwBVRVgBLgCdsnH5MrMGjDtiL2ZJgIIjtpAlATodsbuzPgUuZUmAv8B+K65HvswI8BvYYsVtBn5lSYBHjtjHWRJg1BE7liUB9jhi96ZBgFKMJNZrS3iMuRYI8BaPcaMFAlzDYxSAH00e/q5TpFcYAlabkPxqkh6xD6m3Gtnzx0kYOoHrWrTWszuUFGs+Y9dGJ5MjR47s4Bgwq7e+gpSYyWUGGPDh2V6wwTZRqecDvddnfp7qIj0wuVy23lnsd5FmVWmIacUV5fjMVVlWZS09/xJ4EeOLfeF3WYes/xDOkVoQh+sbP5IbVPiQPo2Qe2seYBTkM3VFj/l1C1C0nt19t7jh9YpejPaVX7cABvuAB45t5YneBPWd3xABHsZsoE/8ugToa8IQLbaQX7cARW0dUYvOkvVHCiTGUgV+aY1gzebXLYDP21pcfiS3HOMgZA4dz2M00Bd+d6WD0IwqzXExrbiqHJ+6KgdUuSwR0nQz1K3kw5uho1HECce2kja7WU2tft0thWtCGqysYR/Z8znIKP4BJe9vzN7fHnUAAAAASUVORK5CYII=" 
                    className="h-12 w-12" 
                    alt="password" 
                />
            </div>
            <div className='w-3/4'>
                <div className="text-xl font-medium text-black">
                    {
                        !loading && password.length <= 0 
                        ? "Password not found!" : 
                        `Your password: ${loading ? "(Loading...)" : ""}`
                    }
                    
                </div>
                {!loading && password.length > 0
                ? (
                    <>
                        {expTime && <span className='text-[10px] absolute top-1 right-1'>Expiration time: {new Date(expTime * 1000).toLocaleString()}</span>}
                        <p className="text-slate-500 bg-gray-100 rounded-md px-2 py-1 mt-2 mb-2">
                            {password}
                        </p>
                        <button
                            className="ml-auto text-right block ml-2 text-slate-500 hover:text-slate-700 focus:outline-none transition duration-150 ease-in-out hover:bg-gray-100 rounded-md px-2 py-1"
                            onClick={() => {
                                navigator.clipboard.writeText(password).then(() => {
                                    Swal.fire({
                                        title: "Copied!",
                                        text: "Password copied to clipboard!",
                                        icon: "success",
                                        toast: true,
                                        timer: 2000,
                                        showConfirmButton: false,
                                        position: "top-end",
                                        timerProgressBar: true,
                                        didOpen: (toast) => {
                                            toast.addEventListener("mouseenter", Swal.stopTimer);
                                            toast.addEventListener("mouseleave", Swal.resumeTimer);
                                        }
                                    });
                                }).catch(() => {
                                    Swal.fire({
                                        title: "Error!",
                                        text: "Failed to copy password to clipboard!",
                                        icon: "error",
                                        toast: true,
                                        timer: 2000,
                                        showConfirmButton: false,
                                        position: "top-end",
                                        timerProgressBar: true,
                                        didOpen: (toast) => {
                                            toast.addEventListener("mouseenter", Swal.stopTimer);
                                            toast.addEventListener("mouseleave", Swal.resumeTimer);
                                        }
                                    });
                                });
                            }}
                        >
                            🔏 Copy
                        </button>
                    </>
                ) : loading ? (
                    <div className="animate-pulse">
                        <div className="h-5 bg-slate-700 rounded"></div>
                    </div>  
                    ) : (<></>)
                }
                
            </div>
        </div>
    );
}