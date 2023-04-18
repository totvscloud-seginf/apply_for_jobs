import * as React from "react";
import { useForm } from "react-hook-form";
import Switch from "react-switch";
import GenPassOptions from "./genPassOptions";
import { setPassword, IPassword } from "../../../app/api/setPassword";
import config from "../../server/config";
import Swal from 'sweetalert2';

export default function GenPassForm(): React.ReactElement {
  const { register, setValue, handleSubmit, formState: { errors }, getValues } = useForm<IPassword>();
  const [viewPassword, setViewPassword] = React.useState<boolean>(false);
  const [dateInDays, setDateInDays] = React.useState<number>(0);

  const onSubmit = handleSubmit((data) => {
    data.valid_until = dateInDays;
    Swal.showLoading();
    setPassword(data, config.app.API_URL).then((res) => {
      const html = `<a className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" href="${config.app.URL}/password/${res.id}">${config.app.URL}/password/${res.id}</a>`;
      Swal.fire({
        title: 'Password Generated',
        html: html,
        icon: 'success',
        confirmButtonText: 'Copy to clipboard',
        preConfirm: () => {
          navigator.clipboard.writeText(`${config.app.URL}/password/${res.id}`).then(() => {
            Swal.fire({
              title: 'Success',
              text: 'Copied to clipboard',
              icon: 'success',
              toast: true,
              position: 'top-end',
              showConfirmButton: false,
              timer: 3000,
              timerProgressBar: true,
              didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
            });
          }).catch((err) => {
            Swal.fire({
              title: 'Error',
              text: 'Error copying to clipboard',
              icon: 'error',
              toast: true,
              position: 'top-end',
              showConfirmButton: false,
              timer: 3000,
              timerProgressBar: true,
              didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
            });
          });
        }
      });
    }).catch((err) => {
      console.log(err);
      Swal.fire({
        title: 'Error',
        text: 'Error generating password',
        icon: 'error',
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      });
    });
  });
  const [isGeneratePass, setIsGeneratePass] = React.useState<boolean>(false);
 
  return (
    <form 
      className="flex flex-col items-center justify-center w-3/4 m-auto h-full mb-10"
      onSubmit={onSubmit}>
      <div className="w-1/2 mb-10 relative">
        <label className="block">Password</label>
        <input
          className="form-input w-full mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400
          focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500
          disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
          invalid:border-pink-500 invalid:text-pink-600
          focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
          type={viewPassword ? "text" : "password"}
          required
          {...register("password", {
            required: true,
          })} 
        />
        <button 
          className="font-bold py-2 px-4 rounded absolute right-2 top-[65%] mt-1 mr-1 transform -translate-y-1/2 h-5 w-5 text-sm flex items-center justify-center"
          type="button"
          onClick={() => setViewPassword(!viewPassword)}
        >
          {!viewPassword ? "🔒" : "🔓"}
        </button>
      </div>
      <div className="w-1/2 mb-10">
        <label className="block">Expiration Date</label>
        <input 
          className="form-input w-full mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400
          focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500
          disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
          invalid:border-pink-500 invalid:text-pink-600
          focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
          type="date"
          {...register("valid_until", {
            validate: (value) => {
              if(!value) return true;
              const date = new Date(value);
              const today = new Date();
              return date >= today;
            },
            onChange: (value) => {
              if(!value) return null;
              const inputDate = new Date(value.target.value);
              const now = new Date();
              const timeDiff = inputDate.getTime() - now.getTime();
              const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
              setDateInDays(daysDiff);
            },
          })} 
        />
      </div>
      <div className="w-1/2 mb-10">
        <label className="block">Views Limit</label>
        <input 
          className="form-input w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400
          focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500
          disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
          invalid:border-pink-500 invalid:text-pink-600
          focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
          type="number"
          value={getValues("view_limit") || 2}
          {...register("view_limit", {
            validate: (value) => {
              return value > 0;
            },
            min: 1,
            valueAsNumber: true,
          })} 
        />
      </div>
      <div className="w-1/2 mb-10">
        <label className="block" >
          <span className="block">Generate Password</span>
          <Switch
            onChange={(checked) => setIsGeneratePass(checked)} 
            checked={isGeneratePass}
          />
        </label>
        {isGeneratePass ? ( <GenPassOptions setValue={setValue} /> ) : null}
      </div>
      
      <input 
        className="rounded-full bg-secondary text-primary font-semibold py-2 px-4 mt-4 hover:border-primary hover:text-gray-800 hover:bg-white cursor-pointer transition duration-200 ease-in-out"
        type="submit" 
      />
    </form>
  );
}