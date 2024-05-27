#include "cppfuns.h"

void cppcluster_c(int *results_ptr, int *Aindex_ptr, double *Asim_ptr, double *times_ptr,int epoches,int c_true, int vnum, int knn){

    unordered_map<int, double> tisum;
    unordered_map<int, double> tifunc;
    Eigen::Map<Arr1ic> results(results_ptr, vnum);
    Eigen::Map<Matir> Aindex(Aindex_ptr, vnum, knn);
    Eigen::Map<Matdr> Asim(Asim_ptr, vnum, knn);
    double isum[c_true] = {0.0};
    for(int j=0;j<vnum;j++){
        int tindex = results(j);
        for(int k=0;k<knn;k++){
            int tmp = Aindex(j,k);
            if((tmp != -1) && (results(tmp) == tindex)){
                double tdis = Asim(j,k);
                isum[tindex] += tdis;
            }
        }
    }
    auto t1 = steady_clock::now();
    for(int t=0;t<epoches;t++){
        int count = 0;
        for(int i=0;i<vnum;i++){
            int old_index = results(i);
            tisum.clear();
            tifunc.clear();
            if(isum[old_index] != 0){
                tisum[old_index] = 0;
                for(int j=0;j<knn;j++){
                    int tmp = Aindex(i,j);
                    if ((tmp != -1) && (tisum.find(results(tmp)) == tisum.end())){
                        tisum[results(tmp)] = 0;
                    }
                }
                for(int j=0;j<knn;j++){
                    int tindex = Aindex(i,j);
                    if(tindex != -1){
                        double tdis = Asim(i,j);
                        tisum[results(tindex)] += tdis;
                    }        
                }
                for(auto keys:tisum){
                    if(keys.first == old_index){
                        tifunc[keys.first] = sqrt(isum[keys.first]) - sqrt(isum[keys.first] - 2*tisum[keys.first]);
                    }
                    else{
                        tifunc[keys.first] = sqrt(isum[keys.first] + 2*tisum[keys.first]) - sqrt(isum[keys.first]);
                    }
                }
                int maxindex = 0;
                double maxvalue = 0.0;
                for(pair<int,double> kv:tifunc){
                    if(maxvalue < kv.second){
                        maxindex = kv.first;
                        maxvalue = kv.second;
                    }
                }
                if(maxindex != old_index){
                    isum[maxindex] += 2*tisum[maxindex];
                    isum[old_index] -= 2*tisum[old_index];
                    results(i) = maxindex;
                    count++;
                }
            }
        }
        float ct = count;
        float vn = vnum;
        if(ct/vn < 0.01){
            break;
        }
    }
    auto t2 = steady_clock::now();
    double ret = chrono::duration<double>(t2 - t1).count();
    //cout << "time = " << ret << endl;
    *times_ptr = ret;
}

void cppcluster_h(int *results_ptr, int *Aindex_ptr, double *Asim_ptr, double *times_ptr, int exptimes, int epoches,int c_true, int vnum, int knn){
    Eigen::Map<Matir> results(results_ptr, exptimes, vnum);
    Eigen::Map<Arr1dc> times(times_ptr, exptimes);
    Eigen::Map<Matir> Aindex(Aindex_ptr, vnum, knn);
    Eigen::Map<Matdr> Asim(Asim_ptr, vnum, knn);
    for(int i=0;i<vnum;i++){
        for(int j=0;j<knn;j++){//A对称化
            int tindex = Aindex(i,j);
            int count = 0;
            for(int k=0;k<knn;k++){
                if(i == Aindex(tindex,k)){
                    count++;
                    break;
                }
            }
            if(count == 0){
                Aindex(i,j) = -1;
                Asim(i,j) = 999.99;
            }
        }
    }
    for(int i = 0;i < exptimes;i++){
        cppcluster_c(&results(i,0), Aindex_ptr, Asim_ptr, &times(i),epoches,c_true,vnum,knn);
    }
}

