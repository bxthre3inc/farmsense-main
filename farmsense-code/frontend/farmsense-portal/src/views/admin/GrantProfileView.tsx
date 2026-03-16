import React from 'react';
import { 
  Landmark, User, MapPin, Droplets, 
  History, ShieldCheck, Save, RefreshCcw 
} from 'lucide-react';
import { useGrantProfile } from '../../data/grant-profile';

export const GrantProfileView: React.FC = () => {
  const { field, setField } = useGrantProfile();

  const sections = [
    {
      id: 'org',
      label: 'Institutional Identity',
      icon: Landmark,
      fields: [
        { key: 'org_name', label: 'Organization Name', placeholder: 'FarmSense Inc.' },
        { key: 'org_legal_name', label: 'Legal Name', placeholder: 'Bxthre3 Inc.' },
        { key: 'ein', label: 'EIN (Tax ID)', placeholder: 'XX-XXXXXXX' },
        { key: 'sam_uei', label: 'SAM.gov UEI', placeholder: 'XXXXXXXXXXXX' },
        { key: 'sam_uei', label: 'SAM.gov UEI', placeholder: 'XXXXXXXXXXXX' },
        { key: 'cage_code', label: 'CAGE Code', placeholder: 'XXXXX' },
      ]
    },
    {
      id: 'pi',
      label: 'Principal Investigator',
      icon: User,
      fields: [
        { key: 'pi_name', label: 'Full Name', placeholder: 'Danny Romero' },
        { key: 'pi_email', label: 'Email Address', placeholder: 'danny@farmsense.ai' },
        { key: 'pi_phone', label: 'Phone Number', placeholder: '+1 (719) XXX-XXXX' },
      ]
    },
    {
      id: 'location',
      label: 'Address & Location',
      icon: MapPin,
      fields: [
        { key: 'org_street', label: 'Street Address', placeholder: '123 Farm Rd' },
        { key: 'org_city', label: 'City', placeholder: 'Center' },
        { key: 'org_state', label: 'State', placeholder: 'CO' },
        { key: 'org_zip', label: 'Zip Code', placeholder: '81125' },
      ]
    }
  ];

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h3 className="text-xl font-black text-slate-900">Organization Profile</h3>
          <p className="text-sm text-slate-500">Auto-persisted data used to pre-fill grant applications.</p>
        </div>
        <div className="flex gap-3">
          <button className="p-3 text-slate-400 hover:text-emerald-500 hover:bg-emerald-50 rounded-xl transition-all">
            <RefreshCcw className="w-5 h-5" />
          </button>
          <div className="bg-emerald-100 text-emerald-700 px-4 py-2 rounded-xl text-xs font-black uppercase flex items-center gap-2">
            <ShieldCheck className="w-4 h-4" />
            Auto-Saving Enabled
          </div>
        </div>
      </div>

      <div className="space-y-12 max-w-4xl">
        {sections.map((section) => (
          <section key={section.id}>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-slate-900 text-white rounded-xl flex items-center justify-center shadow-lg shadow-slate-200">
                <section.icon className="w-5 h-5" />
              </div>
              <h4 className="text-lg font-black text-slate-900">{section.label}</h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50 p-8 rounded-3xl border border-slate-100">
              {section.fields.map((f) => (
                <div key={f.key}>
                  <label className="block text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2 ml-1">
                    {f.label}
                  </label>
                  <input 
                    type="text"
                    value={field(f.key as any)}
                    onChange={(e) => setField(f.key as any, e.target.value)}
                    placeholder={f.placeholder}
                    className="w-full px-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all font-medium text-slate-900"
                  />
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};
