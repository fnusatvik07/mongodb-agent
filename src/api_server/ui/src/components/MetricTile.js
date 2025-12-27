import React from 'react';

const MetricTile = ({ label, value, trend, icon }) => {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-slate-600 mb-1">{label}</p>
          <p className="text-2xl font-semibold text-slate-900">{value}</p>
          {trend && (
            <p className={`text-sm mt-1 ${trend.positive ? 'text-emerald-600' : 'text-red-600'}`}>
              {trend.value}
            </p>
          )}
        </div>
        {icon && (
          <div className="ml-3 flex-shrink-0">
            <div className="w-8 h-8 bg-brand-50 rounded-lg flex items-center justify-center">
              <span className="text-brand-600 text-sm">{icon}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricTile;