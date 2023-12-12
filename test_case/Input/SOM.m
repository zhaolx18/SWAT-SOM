%%%SOM
clear
lr=0.1;          
disp_freq=100;   
max_epoch=1000;  

fileID=fopen('config-SOM.txt','r');
C=textscan(fileID,'%s%s','Delimiter','=');
fclose(fileID);
for i = 1:length(C{1})
    key = C{1}{i};
    value = C{2}{i};
    if strcmp(key, 'RowRange')
        eval([key '=' char(39) value char(39) ';']);  
    else
        eval([key '=' value ';']);  
    end
end

if exist('SOM-results.xls', 'file')
    delete('SOM-results.xls');
end
if exist('SOM-range.xls', 'file')
    delete('SOM-range.xls');
end


W=rands(M,N);                
X0=zeros(N,Q);               
X3=xlsread('data.xlsx',RowRange); 
X0=X3';

XMEAN0=mean(X0');
XSTD0=std(X0');
XMEAN=ones(Q,1)*XMEAN0;
XMEAN=XMEAN';
XSTD=ones(Q,1)*XSTD0;
XSTD=XSTD';
X=(X0-XMEAN)./XSTD;
for q=1:Q
   X(:,q)=X(:,q)/sqrt(X(:,q)'*X(:,q));
end

for m=1:M
   W(m,:)=W(m,:)/sqrt(W(m,:)*W(m,:)');
end

disp('Training begins...')
classification = zeros(Q,1); 
for epoch=1:max_epoch
   for q=1:Q
      for m=1:M
         A(m)=(X(:,q)'-W(m,:))*(X(:,q)-W(m,:)');
      end
      min_d=A(1);j=1;
      for m=2:M
         if A(m)<min_d
            min_d=A(m);j=m;
         end
      end
      classification(q) = j; 
      lr=0.7*(1-((epoch-1)*Q+q-1)/(max_epoch*Q));
      garma=1.7*(1-((epoch-1)*	Q+q-1)/(max_epoch*Q));
      rowj=fix((j-1)/M)+1;
      colj=rem(j-1,M)+1;
      for m=1:M
         rowm=fix((m-1)/M)+1;
         colm=rem(m-1,M)+1;
         dist=sqrt((rowj-rowm)^2+(colj-colm)^2);
        
         if(dist<garma)
            W(m,:)=W(m,:)+lr*(X(:,q)'-W(m,:));
            W(m,:)=W(m,:)/sqrt(W(m,:)*W(m,:)');
         end
      end
   end
   
   if (rem(epoch,disp_freq)==0)
      fprintf('\nEpoch=%5.0f\n',epoch);
   end
end

disp('');
result = [X3, classification, classification*(1/M)]; 
sorted_result = sortrows(result, size(result,2)-1);
sorted_result = [(1:size(sorted_result,1))', sorted_result];
xlswrite('SOM-results.xls', sorted_result);

figure;
plot(sorted_result(:,1), sorted_result(:,end-2), '-', sorted_result(:,1), sorted_result(:,end), '-*');
xlabel('sample');
ylabel('objective function');
grid on;

input_num = input('Please enter the best category: ');

if input_num > M || input_num < 1
    disp('Exceed the number of categories');
else
    filtered_data = sorted_result(sorted_result(:,end-1) == input_num, :);
    
    max_vals = max(filtered_data);
    min_vals = min(filtered_data);
[num, txt, raw] = xlsread('data.xlsx');  
parameter_names = txt(1,1:end-1);
    xlswrite('SOM-range.xls', filtered_data);
    xlswrite('SOM-range.xls', {'MAX:'}, 1, ['A' num2str(size(filtered_data,1)+3)]);
    xlswrite('SOM-range.xls', max_vals, 1, ['A' num2str(size(filtered_data,1)+4)]);
    xlswrite('SOM-range.xls', {'MIN:'}, 1, ['A' num2str(size(filtered_data,1)+5)]);
    xlswrite('SOM-range.xls', min_vals, 1, ['A' num2str(size(filtered_data,1)+6)]);
    xlswrite('SOM-range.xls', parameter_names, 1, ['B' num2str(size(filtered_data,1)+7)]);
    
    disp('saved successfully');
    return;
end
